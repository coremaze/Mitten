from Packets.JoinPacket import JoinPacket
from Packets.ChatPacket import ChatPacket
from Packets.VersionPacket import VersionPacket
from Mitten.Constants import *
import time

aBannedConnections = {}

def HandlePacket(connection, packet, fromClient):
    global aBannedConnections
    if type(packet) == JoinPacket:
        IP = connection.ClientIP()
        if IsBanned(IP):
            aBannedConnections[connection] = True
            print(f'{IP} Is banned and thinks we care about his packets')
            return
    if aBannedConnections.get(connection, False) is True and fromClient is True:
        return BLOCK
    elif aBannedConnections.get(connection, False) is True:
        return



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
