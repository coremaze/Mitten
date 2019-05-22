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

        pickups = []

        
        #gold
        itemid = 12
        itemsubid = 0
        level = int(float(amount) / 10000)
        material = 11 #gold
        item = Item(itemid, itemsubid, 2162, 0, 0, 0,
                 material, 0, 0, level, 0, [Spirit(0,0,0,0,0,0) for _ in range(32)], 0)
        amount = int(fmod(amount, 10000))
        pickups.append(Pickup(GUIDS[connection], item))

        #silver
        itemid = 12
        itemsubid = 0
        level = int(float(amount) / 100)
        material = 12 #silver
        item = Item(itemid, itemsubid, 2162, 0, 0, 0,
                 material, 0, 0, level, 0, [Spirit(0,0,0,0,0,0) for _ in range(32)], 0)
        amount = int(fmod(amount, 100))
        pickups.append(Pickup(GUIDS[connection], item))

        #copper
        itemid = 12
        itemsubid = 0
        level = amount
        material = 10 #copper
        item = Item(itemid, itemsubid, 2162, 0, 0, 0,
                 material, 0, 0, level, 0, [Spirit(0,0,0,0,0,0) for _ in range(32)], 0)
        pickups.append(Pickup(GUIDS[connection], item))


        sup = ServerUpdatePacket([], [], [], [], [], [], {}, {}, pickups, [], [], [], [])
        sup.Send(connection, toServer=False)

def HandleJoin(connection, packet, fromClient):
    global GUIDS
    GUIDS[connection] = packet.creatureID
