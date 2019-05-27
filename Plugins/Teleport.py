from Mitten.Constants import *
from Mitten.Events import *
from Mitten.Alloc import *
from Packets import *
from CubeTypes import *
import time
from threading import Thread
import random

class Player:
    def __init__(self, connection):
        self.connection = connection
        self.position = LongVector3()
        self.guid = -1
        self.teleporter = None
        self.savedCreatures = {}
        self.updatingGUIDs = set()
        self.name = ''
        self.spawnPoint = LongVector3(32800*BLOCK_SCALE, 32800*BLOCK_SCALE, 20*BLOCK_SCALE)

    def SetPosition(self, position):
        self.position = position.Copy()

    def SetGUID(self, guid):
        self.guid = guid

    def FinishUpdate(self):
        #remove unupdated creatures
        newGUIDs, self.updatingGUIDs = self.updatingGUIDs, set()
        for guid in set(self.savedCreatures) - newGUIDs:
            del self.savedCreatures[guid]

    def UpdateCreatures(self, creat):
        self.updatingGUIDs.add(creat.guid)
        if creat.guid not in self.savedCreatures:
            self.savedCreatures[creat.guid] = creat.fields
        else:
            self.savedCreatures[creat.guid].update(creat.fields)

    def _FinishTeleport(self, position):
        while True:
            horizontalPos = self.position.Copy()
            horizontalPos.z = 0
            horizontalDest = position.Copy()
            horizontalDest.z = 0
            #Send GUID 0 creature
            self.teleporter.Send(self.connection, toServer=False)
            if not horizontalPos.Dist(horizontalDest) > BLOCK_SCALE * 1: break

        #Despawn GUID 0 creature
        CreatureUpdateFinishedPacket().Send(self.connection, toServer=False)
        CreatureUpdateFinishedPacket().Send(self.connection, toServer=False)

        #spawn all other creatures
        for guid, fields in self.savedCreatures.items():
            CreatureUpdatePacket(guid=guid, fields=fields).Send(self.connection, toServer=False)
            
        #We do not send a CreatureUpdateFinishedPacket here because the server may be in the middle
        #of sending creatures. If we send a CreatureUpdateFinishedPacket here, it may cause the creatures
        #which the server has already sent to despawn, and then be respawned without appropriate settings.
        #Those settings are also why we memorize all the attributes for creatures instead of just location.
            
        self.teleporter = None
        
    def Teleport(self, position):
        self.teleporter = CreatureUpdatePacket(guid=0, fields={'position':position})
        
        soundUpdate = ServerUpdatePacket()
        
        soundUpdate.sounds.append(Sound(
            position = FloatVector3(self.position.x/BLOCK_SCALE, self.position.y/BLOCK_SCALE, self.position.z/BLOCK_SCALE),
            ID = SOUND_IDS['drop-coin'],
            pitch = random.uniform(0.3, 0.4),
            volume = 0.5))

        soundUpdate.sounds.append(Sound(
            position = FloatVector3(self.position.x/BLOCK_SCALE, self.position.y/BLOCK_SCALE, self.position.z/BLOCK_SCALE),
            ID = SOUND_IDS['manashield'],
            pitch = random.uniform(0.7, 1.2),
            volume = 0.5))
        
        soundUpdate.Send(self.connection, toServer=False)
        
        #Despawn all other creatures        
        CreatureUpdateFinishedPacket().Send(self.connection, toServer=False)
        CreatureUpdateFinishedPacket().Send(self.connection, toServer=False)

        #A thread is needed because we should ensure that the player
        #arrives at the destination.
        #Therefore, we must have the player send more packets to us,
        #which requires that we return from this thread.
        Thread(target=self._FinishTeleport, args=[position]).start()


class World:
    def __init__(self):
        self.players = []
        self.chatGUID = GetGUID()

    def AddPlayer(self, player):
        if type(player) is Player:
            self.players.append(player)
        else:
            player = Player(player)
            self.players.append(player)

    def RemovePlayer(self, player):
        if type(player) is Player:
            self.players.remove(player)
        else:
            players = [x for x in self.players if x.connection is player]
            for player in players:
                self.players.remove(player)

    def GetPlayerNames(self):
        return [x.name for x in self.players]

    def GetPlayerByName(self, name):
        players = [x for x in self.players if x.name.lower() == name.lower()]
        if players:
            return players[0]

    def GetPlayerByConnection(self, connection):
        players = [x for x in self.players if x.connection is connection]
        if players:
            return players[0]

    def HandleJoinPacket(self, connection, packet, fromClient):
        if fromClient: return BLOCK
        player = self.GetPlayerByConnection(connection)
        if player is not None:
            player.guid = packet.creatureID

    def HandleChatPacket(self, connection, packet, fromClient):
        if not fromClient: return
        player = self.GetPlayerByConnection(connection)
        msg = packet.message.lower()
        if msg.startswith('!tpz '):
            try:
                zoneX, zoneY = tuple(map(int, msg.split()[1:3]))
            except:
                self.SendMessage(f'Usage: !tpz <zone x> <zone y>', player)
            else:
                x = zoneX * ZONE_SCALE
                y = zoneY * ZONE_SCALE
                z = 0
                player.Teleport(LongVector3(x,y,z))
            finally:
                return BLOCK

        if msg.startswith('!goto '):
            name = msg[len('!goto '):]
            if name == '':
                self.SendMessage(f'Usage: !goto <player name>', player)
                return BLOCK
            otherPlayer = self.GetPlayerByName(name)
            if otherPlayer is None:
                self.SendMessage(f'Could not find {name}.', player)
            else:
                self.SendMessage(f'Teleporting to {name}!', player)
                player.Teleport(otherPlayer.position - LongVector3(0,0,BLOCK_SCALE*3))
            return BLOCK

        if msg == '!listplayers':
            self.SendMessage('Players: ' + ', '.join(self.GetPlayerNames()), player)
            return BLOCK

        if msg == '!tpspawn':
            player.Teleport(player.spawnPoint)
            return BLOCK

        

    def HandleCreatureUpdatePacket(self, connection, packet, fromClient):
        player = self.GetPlayerByConnection(connection)
        if player is not None:
            if fromClient:
                player.position = packet.fields.get('position', player.position)
                player.name = packet.fields.get('name', player.name)
            else:
                while player.teleporter is not None: pass
                player.UpdateCreatures(packet)

    def HandleCreatureUpdateFinishedPacket(self, connection, packet, fromClient):
        if fromClient: return BLOCK
        player = self.GetPlayerByConnection(connection)
        if player is not None:
            while player.teleporter is not None: pass
            player.FinishUpdate()

    def SendMessage(self, message, player):
        ChatPacket(message, self.chatGUID).Send(player.connection, toServer=False)

world = World()

@Handle(OnConnect)
def HandleConnect(connection):
    world.AddPlayer(connection)

@Handle(OnDisconnect)
def HandleDisconnect(connection):
    world.RemovePlayer(connection)

@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    if type(packet) is JoinPacket:
        return world.HandleJoinPacket(connection, packet, fromClient)
    if type(packet) is ChatPacket:
        return world.HandleChatPacket(connection, packet, fromClient)
    if type(packet) is CreatureUpdatePacket:
        return world.HandleCreatureUpdatePacket(connection, packet, fromClient)
    if type(packet) is CreatureUpdateFinishedPacket:
        return world.HandleCreatureUpdateFinishedPacket(connection, packet, fromClient)
    
        
