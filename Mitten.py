import Packets
import socket
from threading import Thread
import struct
import Plugins
PACKETS_CLASSES = Packets.classes

INTERNAL_SERVER = ('localhost', 12344)
EXTERNAL_SERVER = ('', 12345)

class Connection():
    def __init__(self, clientSock, serverSock, address, port):
        self.clientSock = clientSock
        self.serverSock = serverSock
        self.clientAddress = address
        self.clientPort = port
        self.closed = False
        self.joined = False
        
    def SendServer(self, data):
        try: self.serverSock.sendall(data)
        except: self.Close()
        
    def SendClient(self, data):
        try: self.clientSock.sendall(data)
        except: self.Close()
        
    def RecvServer(self, size):
        buf = b''
        try:
            while len(buf) < size:
                buf += self.serverSock.recv(size - len(buf))
        except:
            self.Close()
        return buf
    
    def RecvClient(self, size):
        buf = b''
        if not self.joined:
            self.clientSock.settimeout(1.0)
        else:
            self.clientSock.settimeout(None)
        try:
            while len(buf) < size:
                buf += self.clientSock.recv(size - len(buf))
        except:
            self.Close()
        return buf

    def ClientIP(self):
        return self.clientAddress
    
    def HandleClient(self):
        while not self.closed:
            try:
                pID, = struct.unpack('<I', self.RecvClient(4))

                #Find the class for this packet
                for packet in PACKETS_CLASSES:
                    if packet.pID == pID:
                        thisClass = packet
                        break
                else:
                    print(f'Invalid packet ID from Client: {pID}')
                    self.Close()
                packet = thisClass.Recv(self, fromClient=True)
                self.joined = True

                for plugin in Plugins.pluginList:
                    if plugin.HandlePacket(self, packet, fromClient=True):
                        print(f'[FROM CLIENT] Canceling a packet pID {pID}')
                        break
                else:
                    #Export and send
                    packet.Send(self, toServer=True)
            except:
                if not self.closed:
                    raise
                
            
            
    def HandleServer(self):
        while not self.closed:
            try:
                pID, = struct.unpack('<I', self.RecvServer(4))
                
                #Find the class for this packet
                for packet in PACKETS_CLASSES:
                    if packet.pID == pID:
                        thisClass = packet
                        break
                else:
                    print(f'Invalid packet ID from Client: {pID}')
                    self.Close()
                packet = thisClass.Recv(self, fromClient=False)

                for plugin in Plugins.pluginList:
                    if plugin.HandlePacket(self, packet, fromClient=False):
                        print(f'[FROM SERVER] Canceling a packet pID {pID}')
                        break
                else:
                    #Export and send
                    packet.Send(self, toServer=False)
            except:
                if not self.closed:
                    raise
            
            
    def Close(self):
        print(f'Closing connection to {self.ClientIP()}.')
        self.closed = True
        try: self.clientSock.close()
        except Exception as e: print(e)
        try: self.serverSock.close()
        except Exception as e: print(e)

if __name__ == '__main__':
    listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSock.bind((EXTERNAL_SERVER))
    while True:
        #Accept connection from client
        listenSock.listen(1)
        clientSock, clientAddr = listenSock.accept()
        print(f'Received a client connection from {clientAddr}.')

        #Make a connection to the server
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'Attempting to connect to server.')
        serverSock.connect((INTERNAL_SERVER))
        print(f'Connected to server.')

        address, port = clientAddr
        connection = Connection(clientSock, serverSock, address, port)

        #Create threads for each of these connections
        Thread(target=Connection.HandleClient, args=[connection]).start()
        print('Client handler started.')
        Thread(target=Connection.HandleServer, args=[connection]).start()
        print('Server handler started.')
