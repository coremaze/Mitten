from Mitten.Constants import *
from Packets import *
from Mitten.Events import *
from CubeTypes import *
from math import fmod

GUIDS = {}

@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    if type(packet) == ChatPacket:
        return HandleChat(connection, packet, fromClient)
    if type(packet) == JoinPacket:
        return HandleJoin(connection, packet, fromClient)

@Handle(OnConnect)
def HandleConnect(connection):
    GUIDS[connection] = 0

@Handle(OnDisconnect)
def HandleDisconnect(connection):
    del GUIDS[connection]

def HandleChat(connection, packet, fromClient):
    if not fromClient:
        return
    message = packet.message.lower()
    if message.startswith('!coins'):
        try:
            amount = int(message.split(' ')[1])
        except:
            return

        #create coins to add up to what the player wants
        pickups = []
        for material, coinScale in ((11, 10000), (12, 100), (10, 1)):
            item = Item()
            item.itemType = 12 #coin
            item.subType = 0
            item.level = int(float(amount) / coinScale)
            item.material = material
            amount = int(fmod(amount, coinScale))
            pickups.append(Pickup(GUIDS[connection], item))

        sup = ServerUpdatePacket()
        sup.pickups = pickups
        sup.Send(connection, toServer=False)

def HandleJoin(connection, packet, fromClient):
    global GUIDS
    GUIDS[connection] = packet.creatureID
