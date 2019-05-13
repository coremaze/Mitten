from Packets.ChatPacket import ChatPacket
from Packets.JoinPacket import JoinPacket
from Packets.EntityUpdatePacket import EntityUpdatePacket
from CubeTypes import CreatureDelta
from CubeTypes import LongVector3
from CubeTypes import FloatVector3
from CubeTypes import Appearance
import time
from copy import deepcopy

DOTS_IN_BLOCK = 65536
BLOCKS_IN_ZONE = 256

joinPackets = {}  # keyed by connection
lastPosition = {} # keyed by connection
latestEntites = {} # keyed by entity_id

def HandlePacket(connection, packet, fromClient):
    if type(packet) == ChatPacket:
        return HandleChatPacket(connection, packet, fromClient)
    elif type(packet) == JoinPacket:
        return HandleJoinPacket(connection, packet, fromClient)
    elif type(packet) == EntityUpdatePacket:
        return HandleEntityUpdatePacket(connection, packet, fromClient)

def HandleJoinPacket(connection, packet, fromClient):
    if connection not in joinPackets:
        joinPackets[connection] = packet

        # Get intial position before entity updates.
        lastPosition[connection] = packet.creature.position
    
def HandleEntityUpdatePacket(connection, packet, fromClient):
    if fromClient:
        # Save the client's last position
        if 'position' in packet.creatureDelta.fields:
            lastPosition[connection] = packet.creatureDelta.fields['position']

    # from server
    else:
        entity_id = packet.creatureDelta.entity_id

        # Block normal GUID 0 bug.
        if entity_id == 0: return

        # Save a local copy of the entites via their delta updates.
        # TODO(Andoryuuta): Find out when to delete these.
        fieldsCopy = deepcopy(packet.creatureDelta.fields)
        if entity_id in latestEntites:
            latestEntites[entity_id].update(fieldsCopy)
        else:
            latestEntites[entity_id] = fieldsCopy


def teleport(connection, x, y, z):
    # Abuse the GUID 0 bug to teleport the user
    newPacket = EntityUpdatePacket(CreatureDelta(0, {'position': LongVector3(x, y, z), 'HP': 1.0}))
    newPacket.Send(connection, toServer=False)

    # The creature needs to stay alive for a short period of time so that the
    # pet update loop teleports us to our "parent_owner" (guid 0 in this case)
    # because we are out of range.

    # Sleeping the entire thread here isn't great, a better approach might
    # to reimplement something akin to javascript's setTimeout function
    # to send the kill packet from another thread later.
    #
    # But meh. ¯\_(ツ)_/¯
    time.sleep(1)

    # Then we kill it to be free.
    newPacket = EntityUpdatePacket(CreatureDelta(0, {'HP': 0.0}))
    newPacket.Send(connection, toServer=False)

    # Now the client will think that _every_ entity has teleported to the GUID 0 entity,
    # so we send the last known position for every we have.
    for entity_id, fields in latestEntites.items():
        EntityUpdatePacket(CreatureDelta(entity_id, {'position': fields['position']})).Send(connection, toServer=False)

    
def HandleChatPacket(connection, packet, fromClient):
    if not fromClient: return

    split = packet.message.lower().split()

    if split[0] == '!tpch':
        cmd, x, y = split
        x = int(x) * DOTS_IN_BLOCK * BLOCKS_IN_ZONE
        y = int(y) * DOTS_IN_BLOCK * BLOCKS_IN_ZONE
        z = 0
        teleport(connection, x, y, z)
        return True

    elif split[0] == '!tp':
        cmd, x, y, z = split
        x = int(x) * DOTS_IN_BLOCK
        y = int(y) * DOTS_IN_BLOCK
        z = int(z) * DOTS_IN_BLOCK
        teleport(connection, x, y, z)
        return True

    elif split[0] == '!tpspawn':
        spawn = joinPackets[connection].creature.spawnPosition
        teleport(connection, spawn.x, spawn.y, spawn.z)
        return True

    elif split[0] == '!blockpos':
        if connection in lastPosition:
            pos = lastPosition[connection]
            x = int(pos.x / DOTS_IN_BLOCK)
            y = int(pos.y / DOTS_IN_BLOCK)
            z = int(pos.z / DOTS_IN_BLOCK)
            ChatPacket(f'[Mitten] Block pos X:{x} Y:{y} Z:{z}', 0).Send(connection, toServer=False)
        return True

    elif split[0] == '!chunkpos':
        if connection in lastPosition:
            pos = lastPosition[connection]
            x = int(pos.x / DOTS_IN_BLOCK / BLOCKS_IN_ZONE)
            y = int(pos.y / DOTS_IN_BLOCK / BLOCKS_IN_ZONE)
            z = int(pos.z / DOTS_IN_BLOCK / BLOCKS_IN_ZONE)
            ChatPacket(f'[Mitten] Chunk pos X:{x} Y:{y} Z:{z}', 0).Send(connection, toServer=False)
        return True

    elif split[0] == '!listplayers':
        playerNames = []
        for entity_id, fields in latestEntites.items():
            if 'name' in fields and fields['name'] != "":
                playerNames.append(fields['name'])

        if len(playerNames) > 0:
            chatStr = '[Mitten] Players: ' + ', '.join(playerNames)
        else:
            chatStr = '[Mitten] No other players online.'

        ChatPacket(chatStr, 0).Send(connection, toServer=False)
        return True

    elif split[0] == '!goto':
        cmd, playerName = split

        # Go over each entity we have and check if the name matches
        for entity_id, fields in latestEntites.items():
            if 'name' in fields and fields['name'] != "":
                if fields['name'].lower() == playerName.lower():
                    # Name matches, teleport to their position

                    ChatPacket(f'[Mitten] Teleporting to {playerName}!', 0).Send(connection, toServer=False)

                    pos = fields['position']
                    teleport(connection, pos.x, pos.y, 0)
                    return True

        # No player was found
        ChatPacket(f'[Mitten] Player {playerName} not found.', 0).Send(connection, toServer=False)