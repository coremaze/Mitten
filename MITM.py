import Packets
import socket
from threading import Thread
PACKETS_CLASSES = Packets.classes

INTERNAL_SERVER = ('localhost', 12344)
EXTERNAL_SERVER = ('', 12345)

def ClientHandler(clientSock, serverSock):
    while True:
        serverSock.send(clientSock.recv(1024))

def ServerHandler(clientSock, serverSock):
    while True:
        clientSock.send(serverSock.recv(1024))

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

        #Create threads for each of these connections
        Thread(target=ClientHandler, args=[clientSock, serverSock]).start()
        Thread(target=ServerHandler, args=[clientSock, serverSock]).start()
