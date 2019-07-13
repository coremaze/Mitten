import Packets
import socket
from threading import Thread
import struct
from Mitten import Configs
import Plugins
import time
from Mitten.Constants import *
from Mitten.Events import *
PACKETS_CLASSES = Packets.classes

INTERNAL_SERVER = tuple(Configs.GetAttribute('Mitten', 'server', ('localhost', 12344)))
EXTERNAL_SERVER = ('', 12345)


class ConnectionPacketCache():
    def __init__(self, connection):
        self.connection = connection
        self._rawData = []
        
    def RecvServer(self, size):
        data = self.connection.RecvServer(size)
        self._rawData.append(data)
        return data

    def RecvClient(self, size):
        data = self.connection.RecvClient(size)
        self._rawData.append(data)
        return data

    def GetRawData(self):
        return b''.join(self._rawData)

class Connection():
    connections = []
    def __init__(self, clientSock, serverSock, address, port):
        self.clientSock = clientSock
        self.serverSock = serverSock
        self.clientAddress = address
        self.clientPort = port
        self.closed = False
        self.joined = False
        self.connections.append(self)
        #Handle new connection
        for handler in MITTEN_EVENTS[OnConnect]:
            handler(self)
        
    def SendServer(self, data):
        try:
            self.serverSock.sendall(data)
        except OSError as e:
            self.Close()
        
    def SendClient(self, data):
        try:
            self.clientSock.sendall(data)
        except OSError as e:
            self.Close()
        
    def RecvServer(self, size):
        buf = []
        total = 0
        while len(buf) < size and not self.closed:
            data = self.serverSock.recv(size - total)
            total += len(data)
            buf.append(data)
        if total != size: raise ConnectionResetError("Could not recv full length")
        return b''.join(buf)

    def RecvClientWatcher(self, timeout=1.0):
        initialTime = time.time()
        time.sleep(timeout)
        if not self.joined:
            self.Close()
    
    def RecvClient(self, size):
        if not self.joined:
            self.clientSock.settimeout(1.0)
            Thread(target=self.RecvClientWatcher).start()
        else:
            self.clientSock.settimeout(None)
        buf = []
        total = 0
        while len(buf) < size and not self.closed:
            data = self.clientSock.recv(size - total)
            total += len(data)
            buf.append(data)
        if total != size: raise ConnectionResetError("Could not recv full length")
        return b''.join(buf)

    def ClientIP(self):
        return self.clientAddress

    def HandleAndSendPacket(self, packet, cache, fromClient):
        modified = False
        #Pass packet to every plugin
        for packetHandler in MITTEN_EVENTS[OnPacket]:
            result = packetHandler(self, packet, fromClient=fromClient)
            if self.closed:
                return
            if result is BLOCK:
                #print(f'[FROM CLIENT] Canceling a packet pID {pID}')
                break
            modified |= result is MODIFY
        else:
            if modified:
                #Export and send
                packet.Send(self, toServer=fromClient)
            else:
                #Send original data
                [self.SendClient, self.SendServer][fromClient](cache.GetRawData())
    
    def HandleClient(self):
        while not self.closed:
            #Keep track of original packet data, so we don't have to export anything if unchanged
            cache = ConnectionPacketCache(self)
            
            try:
                pIDdata = cache.RecvClient(4)
            except Exception as e:
                self.Close()
                break
            else:
                if self.closed: break

            pID, = struct.unpack('<I', pIDdata)

            #Find the class for this packet
            thisClass = self.FindPacketClass(pID, fromClient=True)
            if self.closed: break

            #Get and parse the rest of the packet
            try:
                packet = thisClass.Recv(cache, fromClient=True)
                #Keep track of whether the client sends a packet,
                #to keep them from holding the main CW server thread
                self.joined = True
                self.HandleAndSendPacket(packet, cache, fromClient=True)
            except (ConnectionResetError, ConnectionAbortedError, TimeoutError) as e:
                self.Close()
                break
            else:
                if self.closed: break
            
    def HandleServer(self):
        while not self.closed:
            #Keep track of whether the packet gets modified, for speed.
            modified = False
            cache = ConnectionPacketCache(self)

            try:
                pIDdata = cache.RecvServer(4)
            except Exception as e:
                self.Close()
                break
            else:
                if self.closed: break
            
            pID, = struct.unpack('<I', pIDdata)
            
            #Find the class for this packet
            thisClass = self.FindPacketClass(pID, fromClient=False)
            if self.closed: break

            #Get and parse the rest of the packet
            try:
                packet = thisClass.Recv(cache, fromClient=False)
                self.HandleAndSendPacket(packet, cache, fromClient=False)
            except (ConnectionResetError, ConnectionAbortedError, TimeoutError) as e:
                self.Close()
                break
            else:
                if self.closed: break
                
    def FindPacketClass(self, pID, fromClient):
        #Find the class for this packet
        for packet in PACKETS_CLASSES:
            if packet.pID == pID:
                return packet
            
        for handler in MITTEN_EVENTS[OnUnknownPacket]:
            result = handler(self, pID, fromClient)
            if result is BLOCK or result is None:
                break
            if issubclass(result, Packets.Packet):
                return result
            
        print(f"Invalid packet ID from {['Server', 'Client'][fromClient]}: {pID}")
        self.Close()
                
    def Close(self):
        if not self.closed:
            self.closed = True
            self.connections.remove(self)
            #Handle disconnection
            for handler in MITTEN_EVENTS[OnDisconnect]:
                handler(self)
        try: self.clientSock.close()
        except Exception as e: print(e)
        try: self.serverSock.close()
        except Exception as e: print(e)

    def StartHandlers(self):
        Thread(target=self.HandleClient).start()
        Thread(target=self.HandleServer).start()


def ListenBind(server):
    listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSock.bind(server)
    return listenSock

def MakeServerConnection(server):
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serverSock.connect(server)
    except ConnectionRefusedError:
        if len(MITTEN_EVENTS[OnServerFailure]) == 0:
            print("WARNING: Mitten failed to connect to the internal server, and there are no handlers for this.")
        for handler in MITTEN_EVENTS[OnServerFailure]:
            handler(serverSock, INTERNAL_SERVER)
    return serverSock

def AcceptClient(listenSock):
    listenSock.listen(1)
    clientSock, clientAddr = listenSock.accept()
    address, port = clientAddr
    return clientSock, address, port


if __name__ == '__main__':
    listenSock = ListenBind(EXTERNAL_SERVER)
    while True:
        clientSock, address, port = AcceptClient(listenSock)
        server = INTERNAL_SERVER
        for handler in MITTEN_EVENTS[OnForward]:
            result = handler(clientSock, address, port)
            if result is BLOCK:
                break
            if type(result) == tuple:
                server = result
        else:
            serverSock = MakeServerConnection(server)
            connection = Connection(clientSock, serverSock, address, port)
            connection.StartHandlers()
        
