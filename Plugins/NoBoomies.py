from Mitten.Events import *
from Mitten.Constants import *
from Mitten import Configs
from Packets import *
from CubeTypes import *

PLUGIN = __name__.split('.')[-1]
maxBlocksAway = Configs.GetAttribute(PLUGIN, 'maxBlocksAway', (ZONE_SCALE // BLOCK_SCALE) * 2) #Default is 2 zones away

class Player:
    def __init__(self, connection):
        self.connection = connection
        self.guid = 0
        self.position = LongVector3()
        
    def SetPosition(self, position):
        self.position = position.Copy()

    def SetGUID(self, guid):
        self.guid = guid

PLAYERS = []

@Handle(OnConnect)
def HandleConnect(connection):
    PLAYERS.append(Player(connection))

@Handle(OnDisconnect)
def HandleDisconnect(connection):
    global PLAYERS
    PLAYERS = [x for x in PLAYERS if x.connection is not connection]

@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    if type(packet) == CreatureUpdatePacket:
        return HandleCreatureUpdate(connection, packet, fromClient)
    if type(packet) == JoinPacket:
        return HandleJoin(connection, packet, fromClient)

def HandleCreatureUpdate(connection, packet, fromClient):
    if fromClient:
        if 'position' in packet.fields:
            player = [x for x in PLAYERS if x.guid == packet.guid][0]
            player.SetPosition(packet.fields['position'])
    else:
        sourceGUID = packet.guid
        if sourceGUID not in [x.guid for x in PLAYERS]:
            return
        sourcePlayer = [x for x in PLAYERS if x.guid == sourceGUID][0]
        destPlayer = [x for x in PLAYERS if x.connection is connection][0]

        sourceLoc = sourcePlayer.position
        destLoc = destPlayer.position

        if sourceLoc.Dist(destLoc) <= BLOCK_SCALE * maxBlocksAway:
            return
        
        if 'ability' in packet.fields:
            if packet.fields['ability'] == ABILITY_IDS['FireExplosion']:
                del packet.fields['ability']
                return MODIFY

def HandleJoin(connection, packet, fromClient):
    [x for x in PLAYERS if x.connection is connection][0].guid = packet.creatureID
