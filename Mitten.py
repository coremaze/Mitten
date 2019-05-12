import Packets
import socket
from threading import Thread
import struct
import Plugins
PACKETS_CLASSES = Packets.classes

INTERNAL_SERVER = ('localhost', 12344)
EXTERNAL_SERVER = ('', 12345)

class Connection():
    def __init__(self, clientSock, serverSock):
        self.clientSock = clientSock
        self.serverSock = serverSock
        self.closed = False
        
    def SendServer(self, data):
        try: self.serverSock.send(data)
        except: self.Close()
        
    def SendClient(self, data):
        try: self.clientSock.send(data)
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
        try:
            while len(buf) < size:
                buf += self.clientSock.recv(size - len(buf))
        except:
            self.Close()
        return buf
    
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

                for plugin in Plugins.pluginList:
                    if plugin.HandlePacket(self, packet, fromClient=True):
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
                        break
                else:
                    #Export and send
                    packet.Send(self, toServer=False)
            except:
                if not self.closed:
                    raise
            
            
    def Close(self):
        self.closed = True
        try: self.serverSock.close()
        except: pass
        try: self.clientSock.close()
        except: pass

if __name__ == '__main__':
    listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSock.bind((EXTERNAL_SERVER))
    while True:
        #Accept connection from client
        listenSock.listen(1)
        clientSock, clientAddr = listenSock.accept()

        #Make a connection to the server
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.connect((INTERNAL_SERVER))

        connection = Connection(clientSock, serverSock)

        #Create threads for each of these connections
        Thread(target=Connection.HandleClient, args=[connection]).start()
        Thread(target=Connection.HandleServer, args=[connection]).start()
