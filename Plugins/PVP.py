from Mitten.Events import *
from Mitten.Constants import *
from Packets.EntityUpdatePacket import EntityUpdatePacket
from Packets.JoinPacket import JoinPacket
from Packets.ChatPacket import ChatPacket
from Packets.HitPacket import HitPacket
from threading import Thread

PLAYERS = {}

def GetConnectionByID(ID):
    for c, d in PLAYERS.items():
        if d['ID'] == ID:
            return c

def UpdateHostilities():
    for c1, d1 in PLAYERS.items():
        for c2, d2 in PLAYERS.items():
            if not (d1['ID'] and d2['ID']): continue
            h1 = int(d1['team'] is not None and d2['team'] is not None)
            h2 = d1['team'] != d2['team']
            h = h1 and h2
            Thread(target=EntityUpdatePacket(d1['ID'], {'hostility':h}).Send, args=[c2, False]).start()
            Thread(target=EntityUpdatePacket(d2['ID'], {'hostility':h}).Send, args=[c1, False]).start()

@Handle(OnConnect)
def HandleConnection(connection):
    global PLAYERS
    PLAYERS[connection] = {'team': None, 'ID':0}
    print(f'{connection} is joining None')

@Handle(OnDisconnect)
def HandleDisconnect(connection):
    global PLAYERS
    if connection in PLAYERS:
        del PLAYERS[connection]
    
@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    if type(packet) == ChatPacket:
        return HandleChat(connection, packet, fromClient)
    if type(packet) == JoinPacket:
        return HandleJoin(connection, packet, fromClient)
    if type(packet) == EntityUpdatePacket:
        return HandleEntityUpdate(connection, packet, fromClient)
    if type(packet) == HitPacket:
        return HandleHit(connection, packet, fromClient)


def HandleJoin(connection, packet, fromClient):
    if fromClient: return
    PLAYERS[connection]['ID'] = packet.creatureID
    
def HandleChat(connection, packet, fromClient):
    if not fromClient: return
    msg = packet.message.lower()

    cmd = msg.split(' ')
    if len(cmd) != 2: return
    if cmd[0] != '!pvp': return

    team = [cmd[1], None][cmd[1] == 'none']
    PLAYERS[connection]['team'] = team

    UpdateHostilities()


def HandleEntityUpdate(connection, packet, fromClient):
    if fromClient: return
    if 'hostility' not in packet.fields: return
    fromID = packet.entity_id
    otherConn = GetConnectionByID(fromID)
    if otherConn is None: return

    if not (PLAYERS[connection]['ID'] and PLAYERS[otherConn]['ID']): return
    if PLAYERS[connection]['team'] != PLAYERS[otherConn]['team']:
        h1 = int(PLAYERS[connection]['team'] is not None and PLAYERS[otherConn]['team'] is not None)
        h2 = PLAYERS[connection]['team'] != PLAYERS[otherConn]['team']
        packet.fields['hostility'] = h1 and h2
        return MODIFY

def HandleHit(connection, packet, fromClient):
    if not fromClient: return NO_ACTION
    #Block anyone who doesn't have an ID yet
    if not PLAYERS[connection]['ID']: return BLOCK
    #Block if the player is claiming they're an entity they're not
    if PLAYERS[connection]['ID'] != packet.attackerID: return BLOCK
    #Allow if the target is not a player
    if packet.targetID not in [x['ID'] for x in PLAYERS.values()]: return NO_ACTION

    try:
        otherPlayer = PLAYERS[GetConnectionByID(packet.targetID)]
        thisPlayer = PLAYERS[connection]
    except KeyError:
        return BLOCK

    if packet.dmg >= 0:
        #Block if either are not on a team and attacking
        if otherPlayer['team'] is None or thisPlayer['team'] is None: return BLOCK

        #Block if they are on same team and attacking
        if otherPlayer['team'] == thisPlayer['team']: return BLOCK
    else:
        #Allow healing if the recipient is on no team
        if otherPlayer['team'] is None: return NO_ACTION

        #Block if they are on different teams and healing
        if otherPlayer['team'] != thisPlayer['team']: return BLOCK


    return NO_ACTION
