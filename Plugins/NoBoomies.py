from Mitten.Events import *
from Mitten.Constants import *
from Mitten import Configs
from Packets import *
from CubeTypes import *

PLUGIN = __name__.split('.')[-1]
maxBlocksAway = Configs.GetAttribute(PLUGIN, 'maxBlocksAway', (ZONE_SCALE // BLOCK_SCALE) * 1) #Default is 1 zone away

class Player:
    def __init__(self, connection):
        self.connection = connection
        self.guid = 0
        self.position = LongVector3()
        self.ability = 0
        
    def SetPosition(self, position):
        self.position = position.Copy()

    def SetAbility(self, ability):
        self.ability = ability

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
        player = [x for x in PLAYERS if x.guid == packet.guid][0]
        #remember client position
        if 'position' in packet.fields:
            player.SetPosition(packet.fields['position'])
        #remember current ability
        if 'ability' in packet.fields:
            player.SetAbility(packet.fields['ability'])
    else:
        #return if this isn't an abilityTimer update
        if 'abilityTimer' not in packet.fields:
            return
        
        sourceGUID = packet.guid
        
        #return if this is not a player
        if sourceGUID not in [x.guid for x in PLAYERS]:
            return

        #gather information about both players
        sourcePlayer = [x for x in PLAYERS if x.guid == sourceGUID][0]
        destPlayer = [x for x in PLAYERS if x.connection is connection][0]
        sourceLoc = sourcePlayer.position
        destLoc = destPlayer.position

        #return if they are close to the player
        if sourceLoc.Dist(destLoc) <= BLOCK_SCALE * maxBlocksAway:
            return

        if sourcePlayer.ability == ABILITY_IDS['FireExplosion']:
            packet.fields['abilityTimer'] = 1_000_000_000
            return MODIFY


def HandleJoin(connection, packet, fromClient):
    [x for x in PLAYERS if x.connection is connection][0].guid = packet.creatureID
