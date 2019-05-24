from Mitten.Events import *
from Mitten.Constants import *
from Mitten.Alloc import *
from Packets import *
from Packets.CreatureUpdatePacket import DELTA_TYPES
from CubeTypes import *
from threading import Thread

BLOCK_SCALE = 0x10000
ZONE_SCALE = BLOCK_SCALE * 256
REGION_SCALE = ZONE_SCALE * 64
MISSION_SCALE = REGION_SCALE // 8

import math
import time

class UpdateCreature():
    def __init__(self, guid=0):
        self.guid = guid
        self.fields = {}

class Player(UpdateCreature):
    def __init__(self, connection, guid=0):
        super().__init__(guid)
        self.connection = connection
        self.new = True
        self.points = 0
        self.rewardPoints = 0

    def OnJoin(self):
        self.SendEventEntityUpdate()
        self.SendRadiusUpdate()

    def SendEventEntityUpdate(self, field=None):
        if koth.started and koth.eventEntity:
            if field is None:
                update = CreatureUpdatePacket(koth.eventEntity.guid, koth.eventEntity.fields)
            elif field is not False:
                update = CreatureUpdatePacket(koth.eventEntity.guid, {field:koth.eventEntity.fields[field]})
            else:
                update = CreatureUpdatePacket(koth.eventEntity.guid, {})
            update.Send(self.connection, toServer=False)

    def SendRadiusUpdate(self, field=None):
        if koth.started and koth.eventEntity:
            for d in koth.radii:
                if field is None:
                    update = CreatureUpdatePacket(d.guid, d.fields)
                elif field is not False:
                    update = CreatureUpdatePacket(d.guid, {field:d.fields[field]})
                else:
                    update = CreatureUpdatePacket(d.guid, {})
                update.Send(self.connection, toServer=False)
        

            
        
class KingOfTheHill():
    def __init__(self):
        self.players = []
        self.started = False
        self.eventLocation = LongVector3()
        self.eventEntity = None
        self.radii = []
        self.proximity_radius = 1700000 ** 2
        self.mission = None
        self.lastTick = 0
        self.tickFrequency = 5.0
        self.playersInProximity = []
        self.king = None
        self.kingStart = 0
        self.XPPerTick = 0
        self.kingXPBonus = 10
        self.kingPointsPerTick = 0
        self.pointsPerTick = 0
        self.rewardPoints = 10000
        self.chatGUID = GetGUID()

    def GetPlayerByConnection(self, connection):
        matches = [x for x in self.players if x.connection is connection]
        if matches:
            return matches[0]
        
    def Start(self, position):
        if self.started: return
        self.started = True
        print(f"King of the hill mode activated at {position}")
        self.eventLocation = position.Copy()
        self.eventEntity = UpdateCreature(GetGUID())
        self.eventEntity.fields['hostility'] = 2
        self.eventEntity.fields['appearance'] = Appearance()
        self.eventEntity.fields['appearance'].flags = 1<<8
        self.eventEntity.fields['appearance'].scale.Set(3.0, 3.0, 4.0)
        self.eventEntity.fields['appearance'].bodyModel = 2565
        self.eventEntity.fields['appearance'].headScale = 0.0
        self.eventEntity.fields['appearance'].handScale = 0.0
        self.eventEntity.fields['appearance'].footScale = 0.0
        self.eventEntity.fields['appearance'].shoulder2Scale = 0.0
        self.eventEntity.fields['appearance'].weaponScale = 0.0
        self.eventEntity.fields['appearance'].tailScale = 0.0
        self.eventEntity.fields['appearance'].shoulderScale = 0.0
        self.eventEntity.fields['appearance'].wingScale = 0.0
        self.eventEntity.fields['appearance'].bodyOffset.Set(0.0, 0.0, 25.0)
        self.eventEntity.fields['equipment'] = Equipment()
        self.eventEntity.fields['creatureFlags'] = 64
        self.eventEntity.fields['level'] = 2**31 -1
        self.eventEntity.fields['powerBase'] = 0
        self.eventEntity.fields['name'] = 'King ofthe Hill'
        self.eventEntity.fields['position'] = position.Copy()
        self.eventEntity.fields['position'] += LongVector3(0, 0, 100000)
        self.eventEntity.fields['spawnPosition'] = self.eventEntity.fields['position']
        self.eventEntity.fields['HP'] = 10000000000

        radius_ents = 10
        for i in range(radius_ents):
            radius = UpdateCreature(GetGUID())
            radius.fields['hostility'] = 1
            radius.fields['creatureType'] = 136
            radius.fields['appearance'] = Appearance()
            radius.fields['appearance'].flags = 1<<8
            radius.fields['appearance'].scale.Set(1.0, 1.0, 1.5) 
            radius.fields['appearance'].bodyModel = 2475
            radius.fields['appearance'].headScale = 0.0
            radius.fields['appearance'].handScale = 0.0
            radius.fields['appearance'].footScale = 0.0
            radius.fields['appearance'].shoulder2Scale = 0.0
            radius.fields['appearance'].weaponScale = 0.0
            radius.fields['appearance'].tailScale = 0.0
            radius.fields['appearance'].shoulderScale = 0.0
            radius.fields['appearance'].wingScale = 0.0
            radius.fields['appearance'].bodyOffset.Set(0.0, 0.0, 0.0)
            radius.fields['equipment'] = Equipment()
            radius.fields['creatureFlags'] = 64
            radius.fields['level'] = 2**31 -1
            radius.fields['powerBase'] = 0
            radius.fields['name'] = 'King ofthe Hill'
            radius.fields['position'] = self.eventEntity.fields['position'].Copy()
            radius.fields['HP'] = 10000000000

            r = math.pi * 2 / radius_ents * i
            x = math.sqrt(self.proximity_radius) * math.sin(r)
            y = math.sqrt(self.proximity_radius) * math.cos(r)
            radius.fields['position'] = LongVector3(int(x), int(y), 0) + self.eventEntity.fields['position']
            self.radii.append(radius)
            

        for player in self.players:
            Thread(target=player.SendEventEntityUpdate).start()
            Thread(target=player.SendRadiusUpdate).start()


        self.mission = Mission()
        self.mission.regionX = self.eventEntity.fields['position'].x // REGION_SCALE
        self.mission.regionY = self.eventEntity.fields['position'].y // REGION_SCALE
        self.mission.missionID = 1
        self.mission.monsterID = 1000
        self.mission.level = 500
        self.mission.zoneX = self.eventEntity.fields['position'].x // ZONE_SCALE
        self.mission.zoneY = self.eventEntity.fields['position'].y // ZONE_SCALE


    def Update(self, serverupdate):
        if not self.started or not self.eventEntity: return

        if self.mission is not None:
            serverupdate.missions.append(self.mission)

        if (time.time() - self.lastTick > self.tickFrequency):
            self.lastTick = time.time()
            self.DoProximityCheck()
            self.GrantXPAndGold()

    def DoProximityCheck(self):
        bad_items = []
        for player in self.playersInProximity:
            if player not in self.players:
                bad_items.append(player)

        for player in bad_items:
            self.playersInProximity.remove(player)

        for player in self.players:
            distance = (self.eventLocation - player.fields['position']).MagnitudeSquared()

            if distance < self.proximity_radius and player.fields['HP'] > 0:
                if player not in self.playersInProximity:
                    self.playersInProximity.append(player)
            elif player in self.playersInProximity:
                self.playersInProximity.remove(player)

        if len(self.playersInProximity) > 0:
            if self.king is None or self.king.guid != self.playersInProximity[0].guid:
                newKing = self.playersInProximity[0]
                message = f'New king of the hill: {newKing.fields["name"]}'
                chat = ChatPacket(message, self.chatGUID)
                for player in self.players:
                    Thread(target=chat.Send, args=[player.connection, False]).start()

                now = time.time()
                if self.king:
                    message = f'{self.king.fields["name"]} was king for {int(now - self.kingStart)} seconds.'
                    chat = ChatPacket(message, self.chatGUID)
                    for player in self.players:
                        Thread(target=chat.Send, args=[player.connection, False]).start()
                
                self.kingStart = now
                self.king = newKing
                self.eventEntity.fields['name'] = self.king.fields['name']
                print(f'New king of the hill: {self.king.fields["name"]}')

        elif self.king is not None:
            now = time.time()
            message = f'{self.king.fields["name"]} was king for {int(now - self.kingStart)} seconds.'
            chat = ChatPacket(message, self.chatGUID)
            for player in self.players:
                Thread(target=chat.Send, args=[player.connection, False]).start()
                
            self.eventEntity.fields['name'] = 'King ofthe Hill'
            self.king = None


    def GrantXPAndGold(self):pass
##        if len(self.playersInProximity) == 0:
##            return
##
##        for player in self.playersInProximity:
##            xp = self.XPPerTick
##            if player.guid == self.king.guid:
##                xp += self.kingXPBonus
##                player.points += self.kingPointsPerTick
##            else:
##                player.points += self.pointsPerTick
##
##            self.GiveXP(player, xp)
##
##            if player.rewardPoints > self.rewardPoints:
##                player.rewardPoints -= self.rewardPoints
##                print(("{name} has reached {points} points," +
##                           " and receives an additional reward!")
##                           .format(name=player.fields['name'],
##                                   points=self.reward_points))
##            

        
koth = KingOfTheHill()

@Handle(OnConnect)
def HandleConnect(connection):
    global koth
    koth.players.append(Player(connection))

@Handle(OnDisconnect)
def HandleDisconenct(connection):
    player = koth.GetPlayerByConnection(connection)
    if player in koth.players:
        koth.players.remove(player)

@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    if type(packet) == ChatPacket:
        return HandleChat(connection, packet, fromClient)
    if type(packet) == JoinPacket:
        return HandleJoin(connection, packet, fromClient)
    if type(packet) == CreatureUpdatePacket:
        return HandleCreatureUpdate(connection, packet, fromClient)
    if type(packet) == CreatureUpdateFinishedPacket:
        return HandleCreatureUpdateFinished(connection, packet, fromClient)
    if type(packet) == ServerUpdatePacket:
        return HandleServerUpdate(connection, packet, fromClient)

def HandleChat(connection, packet, fromClient):
    if not fromClient: return
    player = koth.GetPlayerByConnection(connection)
    if packet.message.lower() == '!kothstart':
        koth.Start(player.fields['position'])

def HandleJoin(connection, packet, fromClient):
    player = koth.GetPlayerByConnection(connection)
    player.guid = packet.creatureID

def HandleCreatureUpdate(connection, packet, fromClient):
    if fromClient:
        player = koth.GetPlayerByConnection(connection)
        if player.new:
            player.new = False
            player.SendEventEntityUpdate()
            player.SendRadiusUpdate()
        player.fields.update(packet.fields)
    else:
        if packet.entity_id in [x.guid for x in koth.players]:
            if 'hostility' in packet.fields:
                packet.fields['hostility'] = 1
                return MODIFY

def HandleCreatureUpdateFinished(connection, packet, fromClient):
    player = koth.GetPlayerByConnection(connection)
    player.SendEventEntityUpdate('name')
    player.SendRadiusUpdate(False)

def HandleServerUpdate(connection, packet, fromClient):
    koth.Update(packet)
    return MODIFY
    
