from Packets import *
from CubeTypes import LongVector3
from CubeTypes import FloatVector3
from CubeTypes import Appearance
from CubeTypes import Sound
from Mitten.Constants import *
from Mitten.Events import *
import time

DOTS_IN_BLOCK = 65536
BLOCKS_IN_ZONE = 256

latestEntities = {} # keyed by entity_id
players = {} # keyed by connection
spawnPoint = None

@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    #this catastophe can have dicts being modified from other threads while in use
    try:
        #remove old connections
        for c in list(players):
            if c.closed:
                del players[c]

        if connection not in players:
            players[connection] = {'teleport':None}
                
        #Packet-specific handlers
        if type(packet) == ChatPacket:
            return HandleChatPacket(connection, packet, fromClient)
        elif type(packet) == JoinPacket:
            return HandleJoinPacket(connection, packet, fromClient)
        elif type(packet) == CreatureUpdatePacket:
            return HandleCreatureUpdatePacket(connection, packet, fromClient)
    except Exception as e:
        print(e)


def HandleJoinPacket(connection, packet, fromClient):
    global spawnPoint
    if fromClient: return
    spawnPoint = packet.creature.position
    
    
def HandleCreatureUpdatePacket(connection, packet, fromClient):
    global players
    if fromClient:
        player = players[connection]

        fields = packet.fields
        if 'fields' not in player: player['fields'] = fields
        else:                      player['fields'].update(fields)
        
        # Save the client's last position
        if 'position' in fields:
            position = packet.fields['position']
            player['position'] = position
            #Is the player teleporting?
            if player['teleport']:
                destination = player['teleport']
                
                # Don't care about height when teleporting
                x1, y1 = position.x, position.y
                x2, y2 = destination.x, destination.y
                
                # Check to see if the player is there yet
                if LongVector3(x1, y1, 0).Dist(LongVector3(x2, y2, 0)) <= DOTS_IN_BLOCK:
                    player['teleport'] = None
                    # Now the client will think that _every_ entity has teleported to the GUID 0 entity,
                    # so we send the last known position for every we have.
                    for entity_id, fields in list(latestEntities.items()):
                        CreatureUpdatePacket(entity_id, {'position': fields['position']}).Send(connection, toServer=False)

    # from server
    else:
        entity_id = packet.entity_id

        # Block normal GUID 0 bug.
        if entity_id == 0: return BLOCK

        # Save a local copy of the entites via their delta updates.
        # TODO(Andoryuuta): Find out when to delete these.
        if entity_id in latestEntities:
            latestEntities[entity_id].update(packet.fields)
        else:
            latestEntities[entity_id] = packet.fields


def teleport(connection, x, y, z):
    global players
    if connection not in players: return
    players[connection]['teleport'] = LongVector3(x, y, z)
    orgiginalpos = players[connection]['position']
    ServerUpdatePacket([],[],[],[
        Sound(FloatVector3(orgiginalpos.x/65536, orgiginalpos.y/65536, orgiginalpos.z/65536), 58, 0.35, 0.50)
        ],[],[],{},{},[],[],[],[],[]).Send(connection, toServer=False)
    CreatureUpdatePacket(0, {'position': LongVector3(x, y, z)}).Send(connection, toServer=False)

def HandleChatPacket(connection, packet, fromClient):
    global players, spawnPoint
    if not fromClient: return
    if connection not in players: return
    player = players[connection]
    if 'position' not in player: return
    
    split = packet.message.lower().split()
    if not len(split): return

    position = player['position']
    
    try:
        if split[0] == '!tpz':
            cmd, x, y = split
            x = int(x) * DOTS_IN_BLOCK * BLOCKS_IN_ZONE
            y = int(y) * DOTS_IN_BLOCK * BLOCKS_IN_ZONE
            z = 0
            teleport(connection, x, y, z)
            return BLOCK
        
        #Really not needed, or even helpful.
##        elif split[0] == '!tp':
##            cmd, x, y, z = split
##            x = int(x) * DOTS_IN_BLOCK
##            y = int(y) * DOTS_IN_BLOCK
##            z = int(z) * DOTS_IN_BLOCK
##            teleport(connection, x, y, z)
##            return True

        elif split[0] == '!tpspawn':
            if spawnPoint:
                teleport(connection, spawnPoint.x, spawnPoint.y, spawnPoint.z)
            else:
                teleport(connection, 32800 * DOTS_IN_BLOCK * BLOCKS_IN_ZONE, 32800 * DOTS_IN_BLOCK * BLOCKS_IN_ZONE, 0)
            return BLOCK

        elif split[0] == '!blockpos':
            pos = player['position']
            x = int(pos.x / DOTS_IN_BLOCK)
            y = int(pos.y / DOTS_IN_BLOCK)
            z = int(pos.z / DOTS_IN_BLOCK)
            ChatPacket(f'[Mitten] Block pos X:{x} Y:{y} Z:{z}', 0).Send(connection, toServer=False)
            return BLOCK

        elif split[0] == '!zonepos':
            x = int(position.x / DOTS_IN_BLOCK / BLOCKS_IN_ZONE)
            y = int(position.y / DOTS_IN_BLOCK / BLOCKS_IN_ZONE)
            z = int(position.z / DOTS_IN_BLOCK / BLOCKS_IN_ZONE)
            ChatPacket(f'[Mitten] Zone pos X:{x} Y:{y} Z:{z}', 0).Send(connection, toServer=False)
            return BLOCK

        elif split[0] == '!listplayers':
            playerNames = [players[x]['fields']['name'] for x in players
                           if 'fields' in players[x]
                           and 'name' in players[x]['fields']]
                    
            chatStr = '[Mitten] Players: ' + ', '.join(playerNames)
            ChatPacket(chatStr, 0).Send(connection, toServer=False)
            return BLOCK

        elif split[0] == '!goto':
            playerName = ' '.join(split[1:])

            # Go over each entity we have and check if the name matches
            matchingPlayers = [players[x] for x in players
                               if 'fields' in players[x]
                               and 'name' in players[x]['fields']
                               and players[x]['fields']['name'].lower() == playerName.lower()]
            
            if not len(matchingPlayers):
                ChatPacket(f'[Mitten] Found no match for {playerName}.', 0).Send(connection, toServer=False)
                return BLOCK
            
            tpPlayer = matchingPlayers[0]

            if tpPlayer is players[connection]:
                ChatPacket(f'[Mitten] You are already in your location!', 0).Send(connection, toServer=False)
                return BLOCK

            ChatPacket(f'[Mitten] Teleporting to {playerName}!', 0).Send(connection, toServer=False)

            pos = tpPlayer['position']
            teleport(connection, pos.x, pos.y, pos.z-DOTS_IN_BLOCK*4)
            return BLOCK

            # No player was found
            ChatPacket(f'[Mitten] Player {playerName} not found.', 0).Send(connection, toServer=False)
    except (ValueError, IndexError):
        ChatPacket(f'[Mitten] Invalid command: {packet.message}', 0).Send(connection, toServer=False)
        return BLOCK
