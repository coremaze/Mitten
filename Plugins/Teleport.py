from Mitten.Constants import *
from Mitten.Events import *
from Mitten.Alloc import *
from Mitten import Configs
from Packets import *
from CubeTypes import *
import time
from threading import Thread
import random

PLUGIN = __name__.split('.')[-1]

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
        self.teleports = Configs.GetAttribute(PLUGIN, 'teleports', [])
        self.tpsetEnabled = Configs.GetAttribute(PLUGIN, 'tpsetEnabled', True)

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
        if player is None: return
        
        msg = packet.message.lower()

        if self.Command('!tpz', msg, player, self.TPZ): return BLOCK
        if self.Command('!goto', msg, player, self.Goto): return BLOCK
        if self.Command('!listplayers', msg, player, self.ListPlayers): return BLOCK
        if self.Command('!tpset', msg, player, self.TPSet): return BLOCK
        if self.Command('!tp', msg, player, self.TP): return BLOCK
        if self.Command('!tplist', msg, player, self.TPList): return BLOCK

##Commands##
    def Command(self, prefix, msg, player, function):
        #splitting is intensive, so avoid doing it if possible.
        if not msg.startswith(prefix):
            return
        
        split = msg.split()
        msgprefix, arguments = split[0], split[1:]
        if msgprefix == prefix:
            function(arguments, player)
            return True
        return False

    def TPZ(self, arguments, player):
        try:
            zoneX, zoneY = tuple(map(int, arguments))
        except:
            self.SendMessage(f'Usage: !tpz <zone x> <zone y>', player)
        else:
            x = zoneX * ZONE_SCALE
            y = zoneY * ZONE_SCALE
            z = 0
            player.Teleport(LongVector3(x,y,z))

    def Goto(self, arguments, player):
        name = ' '.join(arguments)
        if name == '':
            self.SendMessage(f'Usage: !goto <player name>', player)
        else:
            otherPlayer = self.GetPlayerByName(name)
            if otherPlayer is None:
                self.SendMessage(f'Could not find {name}.', player)
            else:
                self.SendMessage(f'Teleporting to {name}!', player)
                player.Teleport(otherPlayer.position - LongVector3(0,0,BLOCK_SCALE*3))

    def ListPlayers(self, arguments, player):
        self.SendMessage('Players: ' + ', '.join(self.GetPlayerNames()), player)

    def TPSet(self, arguments, player):
        if self.tpsetEnabled:
            try:
                name, = arguments
            except Exception as e:
                self.SendMessage('Usage: !tpset <name>', player)
            else:
                self.SetTeleport(name, player.position)
                self.SendMessage(f'Created teleport {name}', player)

    def TP(self, arguments, player):
        try:
            name, = arguments
        except Exception as e:
            self.SendMessage('Usage: !tp <name>', player)
        else:
            if not name.isalnum():
                self.SendMessage(f'Invalid name {name}', player)
                return
            tp = self.GetTeleport(name)
            if tp is None:
                self.SendMessage(f'Cannot find teleport {name}', player)
                return
            else:
                self.SendMessage(f'Teleporting to {name}!', player)
                player.Teleport(tp)

    def TPList(self, arguments, player):
        resp = 'Teleports: ' + ', '.join(self.GetTeleportNames())
        self.SendMessage(resp, player)
        
##End of commands##
        
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

    def SetTeleport(self, name, location):
        self.teleports.append({'name':name, 'x':location.x, 'y':location.y, 'z':location.z})
        Configs.SetAttribute(PLUGIN, 'teleports', self.teleports)

    def GetTeleport(self, name):
        for tp in self.teleports:
            if tp['name'] == name:
                return LongVector3(tp['x'], tp['y'], tp['z'])

    def GetTeleportNames(self):
        return [x['name'] for x in self.teleports]

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
    
        
