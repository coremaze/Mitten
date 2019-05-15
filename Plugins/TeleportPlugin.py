from Packets.ChatPacket import ChatPacket
from Packets.JoinPacket import JoinPacket
from Packets.EntityUpdatePacket import EntityUpdatePacket
from CubeTypes import CreatureDelta
from CubeTypes import LongVector3
from CubeTypes import FloatVector3
from CubeTypes import Appearance
from Mitten.Constants import *
import time
from copy import deepcopy

DOTS_IN_BLOCK = 65536
BLOCKS_IN_ZONE = 256

latestEntities = {} # keyed by entity_id
players = {} # keyed by connection

def HandlePacket(connection, packet, fromClient):
    #this catastophe can have dicts being modified from other threads while in use
    for retry in range(3):
        try:
            #Make sure to keep the GUID 0 creature alive for the teleporting clients at all times
            if fromClient:
                if connection in players and players[connection]['teleport']:
                    newPacket = EntityUpdatePacket(CreatureDelta(0, {'position': players[connection]['teleport'], 'HP': 1.0}))
                    newPacket.Send(connection, toServer=False)

            #remove old connections
            for c in list(players):
                if c.closed:
                    del players[c]
                    
            #Packet-specific handlers
            if type(packet) == ChatPacket:
                return HandleChatPacket(connection, packet, fromClient)
            elif type(packet) == JoinPacket:
                return HandleJoinPacket(connection, packet, fromClient)
            elif type(packet) == EntityUpdatePacket:
                return HandleEntityUpdatePacket(connection, packet, fromClient)
        except (RuntimeError, KeyError) as e:
            print(e)
        else:
            break


def HandleJoinPacket(connection, packet, fromClient):
    if connection not in players:
        players[connection] = {'teleport':None}
        players[connection]['initialCreature'] = packet.creature
        players[connection]['position'] = packet.creature.position
    
def HandleEntityUpdatePacket(connection, packet, fromClient):
    if fromClient:
        player = players[connection]

        fields = packet.creatureDelta.fields
        if 'fields' not in player:
            player['fields'] = fields
        else:
            player['fields'].update(fields)
        
        # Save the client's last position
        if 'position' in fields:
            position = packet.creatureDelta.fields['position']
            player['position'] = position
            #Is the player teleporting?
            if player['teleport']:
                destination = player['teleport']
                
                # Don't care about height when teleporting
                x1, y1 = position.x, position.y
                x2, y2 = destination.x, destination.y
                
                # Check to see if the player is there yet
                # If so, get rid of the GUID 0 creature
                if LongVector3(x1, y1, 0).Dist(LongVector3(x2, y2, 0)) <= DOTS_IN_BLOCK:
                    player['teleport'] = None
                    newPacket = EntityUpdatePacket(CreatureDelta(0, {'HP': 0.0}))
                    newPacket.Send(connection, toServer=False)
                    # Now the client will think that _every_ entity has teleported to the GUID 0 entity,
                    # so we send the last known position for every we have.
                    for entity_id, fields in list(latestEntities.items()):
                        EntityUpdatePacket(CreatureDelta(entity_id, {'position': fields['position']})).Send(connection, toServer=False)

    # from server
    else:
        entity_id = packet.creatureDelta.entity_id

        # Block normal GUID 0 bug.
        if entity_id == 0: return BLOCK

        # Save a local copy of the entites via their delta updates.
        # TODO(Andoryuuta): Find out when to delete these.
        fieldsCopy = deepcopy(packet.creatureDelta.fields)
        if entity_id in latestEntities:
            latestEntities[entity_id].update(fieldsCopy)
        else:
            latestEntities[entity_id] = fieldsCopy


def teleport(connection, x, y, z):
    players[connection]['teleport'] = LongVector3(x, y, z)

def HandleChatPacket(connection, packet, fromClient):
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
            spawn = players[connection]['initialCreature'].spawnPosition
            teleport(connection, spawn.x, spawn.y, spawn.z)
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
            playerNames = [DecodeString(players[x]['fields']['name']) for x in players if 'name' in players[x]['fields']]
                    
            chatStr = '[Mitten] Players: ' + ', '.join(playerNames)
            ChatPacket(chatStr, 0).Send(connection, toServer=False)
            return BLOCK

        elif split[0] == '!goto':
            playerName = ' '.join(split[1:])

            # Go over each entity we have and check if the name matches
            matchingPlayers = [players[x] for x in players if players[x]['fields']['name'].lower() == playerName.lower()]
            
            if not len(matchingPlayers):
                ChatPacket(f'[Mitten] Found no match for {playerName}.', 0).Send(connection, toServer=False)
                return BLOCK
            
            tpPlayer = matchingPlayers[0]

            if tpPlayer is players[connection]:
                ChatPacket(f'[Mitten] You are already in your location!', 0).Send(connection, toServer=False)
                return BLOCK

            ChatPacket(f'[Mitten] Teleporting to {playerName}!', 0).Send(connection, toServer=False)

            pos = tpPlayer['position']
            teleport(connection, pos.x, pos.y, 0)
            return BLOCK

            # No player was found
            ChatPacket(f'[Mitten] Player {playerName} not found.', 0).Send(connection, toServer=False)
    except (ValueError, IndexError):
        ChatPacket(f'[Mitten] Invalid command: {packet.message}', 0).Send(connection, toServer=False)
        return BLOCK
