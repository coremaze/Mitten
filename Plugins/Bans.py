from Packets.JoinPacket import JoinPacket
from Packets.ChatPacket import ChatPacket
from Packets.VersionPacket import VersionPacket
from Mitten.Constants import *
import time

def IsBanned(IP):
    while True:
        try:
            with open('bans.txt', 'r') as f:
                IPs = [x.strip() for x in f.read().split('\n') if x.strip()]
        except FileNotFoundError:
            with open('bans.txt', 'w') as f:
                pass
        else:
            break

    return IP in IPs

banInProcess = []
def BanKick(connection):
    IP = connection.ClientIP()
    print(f'{IP} tried to connect, but they are banned.')
    newPacket = ChatPacket('You have been banned from this server.', 0)
    newPacket.Send(connection, toServer=False)
    time.sleep(1)
    connection.Close()
    banInProcess = [x for x in banInProcess if x != connection]

def HandlePacket(connection, packet, fromClient):
    IP = connection.ClientIP()
    if fromClient:
        if type(packet) != VersionPacket:
            if IsBanned(IP) and connection not in banInProcess:
                banInProcess.append(connection)
                BanKick(connection)
                return BLOCK
    else:
        if type(packet) == JoinPacket:
            if IsBanned(IP) and connection not in banInProcess:
                banInProcess.append(connection)
                packet.Send(connection, fromClient)
                BanKick(connection)
                return BLOCK

    
    
