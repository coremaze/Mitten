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
import random


REWARD_WEAPONS = dict({
    # Weapons
    (3, 0): (1, ),   # 1h swords only iron
    (3, 1): (1, ),   # axes only iron
    (3, 2): (1, ),   # maces only iron
    (3, 3): (1, ),   # daggers only iron
    (3, 4): (1, ),   # fists only iron
    (3, 5): (1, ),   # longswords only iron
    (3, 6): (2, ),   # bows, only wood
    (3, 7): (2, ),   # crossbows, only wood
    (3, 8): (2, ),   # boomerangs, only wood

    (3, 10): (2, ),  # wands, only wood
    (3, 11): (2, ),     # staffs, only wood
    (3, 12): (11, 12),   # bracelets, silver, gold

    (3, 13): (1, ),    # shields, only iron

    (3, 15): (1, ),    # 2h, only iron
    (3, 16): (1, ),    # 2h, only iron
    (3, 17): (1, 2),   # 2h mace, iron and wood
})

REWARD_ARMOR = dict({
    # Equipment
    # chest warrior (iron), mage (silk), ranger(linen), rogue(cotton)
    (4, 0): (1, 25, 26, 27),
    # gloves warrior (iron), mage (silk), ranger(linen), rogue(cotton)
    (5, 0): (1, 25, 26, 27),
    # boots warrior (iron), mage (silk), ranger(linen), rogue(cotton)
    (6, 0): (1, 25, 26, 27),
    # shoulder warrior (iron), mage (silk), ranger(linen), rogue(cotton)
    (7, 0): (1, 25, 26, 27),
    (8, 0): (11, 12),  # rings, gold and silver
    (9, 0): (11, 12),  # amulets, gold and silver
})

REWARD_MISC = dict({
    (11, 14): (128, 129, 130, 131),
})

REWARD_PET_ITEMS = dict({})

REWARD_PETS = (19, 22, 23, 25, 26, 27, 30, 33, 34, 35, 36, 37, 38, 39, 40, 50,
               53, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 74, 75,
               86, 87, 88, 90, 91, 92, 93, 98, 99, 102, 103, 104, 105, 106,
               151)


# generate pets and petfood in the reward item list based on reward pets
def GeneratePets():
    for pet in REWARD_PETS:
        REWARD_PET_ITEMS[(19, pet)] = (0, )
        REWARD_PET_ITEMS[(20, pet)] = (0, )


GeneratePets()



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
        self.dead = False
        self.announced = False

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
                    fields = d.fields
                elif field is not False:
                    fields = {field:d.fields[field]}
                else:
                    fields = {}
                update = CreatureUpdatePacket(d.guid, fields)
                update.Send(self.connection, toServer=False)


    def SendDummyUpdate(self, field=None):
        if koth.started and koth.eventEntity:
            if field is None:
                update = CreatureUpdatePacket(koth.eventDummy.guid, koth.eventDummy.fields)
            elif field is not False:
                update = CreatureUpdatePacket(koth.eventDummy.guid, {field:koth.eventDummy.fields[field]})
            else:
                update = CreatureUpdatePacket(koth.eventDummy.guid, {})
            update.Send(self.connection, toServer=False)

    def GiveItem(self, item):
        pickup = Pickup(self.guid, item)
        update = ServerUpdatePacket()
        update.pickups.append(pickup)
        Thread(target=update.Send, args=[self.connection, False]).start()

    def AddPoints(self, pts):
        newPoints = self.rewardPoints + pts

        pct = [0.80, 0.60, 0.40, 0.20]
        maxpts = koth.rewardPoints

        for i in range(len(pct)):
            if (newPoints >= pct[i] * maxpts and
                    self.rewardPoints < pct[i] * maxpts):
                self.ShowKothPoints()
                break

        self.rewardPoints = newPoints

    def ShowKothPoints(self):
        maxpts = koth.rewardPoints
        pct = self.rewardPoints / maxpts * 100
        message = f"KotH points {int(self.rewardPoints)}/{int(maxpts)} ({int(pct)}%)"
        Thread(target=ChatPacket(message, koth.chatGUID).Send, args=[self.connection, False]).start()

    def OnKill(self, otherPlayer):
        if koth.king is None:
            return

        if otherPlayer is koth.king:
            message = f'you killed {otherPlayer.fields["name"]} for {koth.killKingPoints}(+{koth.killKingXP}xp) KotH points! (+king bonus)'
            Thread(target=ChatPacket(message, koth.chatGUID).Send, args=[self.connection, False]).start()
            self.AddPoints(koth.killKingPoints)
            koth.GiveXP(self, koth.killKingXP)

        elif otherPlayer in koth.playersInProximity:
            message = f'you killed {otherPlayer.fields["name"]} for {koth.killPoints}(+{koth.killXP}xp) KotH points!'
            Thread(target=ChatPacket(message, koth.chatGUID).Send, args=[self.connection, False]).start()
            self.AddPoints(koth.killPoints)
            koth.GiveXP(self, koth.killXP)
            
        
class KingOfTheHill():
    def __init__(self):
        self.players = []
        self.started = False
        self.eventLocation = LongVector3()
        self.eventEntity = None
        self.eventDummy = None
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
        self.kingPointsPerTick = 500 #0
        self.pointsPerTick = 100 #0
        self.rewardPoints = 10000
        self.chatGUID = GetGUID()
        self.maxLevel = 0
        self.copperPerTick = 10 #0
        self.itemDropRadius = 1000000
        self.killKingPoints = 500
        self.killPoints = 100
        self.killKingXP = 100
        self.killXP = 50

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
        self.eventEntity.fields['hostility'] = 0 #2
        self.eventEntity.fields['appearance'] = Appearance()
        self.eventEntity.fields['appearance'].flags = 1<<8
        self.eventEntity.fields['appearance'].scale.Set(3.0, 3.0, 4.0)
        self.eventEntity.fields['appearance'].bodyModel = 2565
        self.eventEntity.fields['appearance'].headModel = 2470
        self.eventEntity.fields['appearance'].hairModel = 0xFFFF
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



        # Create a dummy entity that is hostile, only way
        # HitPacket will grant xp
        if self.eventDummy is None:
            self.eventDummy = UpdateCreature(GetGUID())
            self.eventDummy.fields['hostility'] = 1
            self.eventDummy.fields['position'] = LongVector3(0, 0, 65536*10) + self.eventEntity.fields['position']
            self.eventDummy.fields['spawnPosition'] = self.eventEntity.fields['position']
            self.eventDummy.fields['HP'] = 10000000000
            self.eventDummy.fields['powerBase'] = 1
            self.eventDummy.fields['name'] = 'KOTHDummy!'
            self.eventDummy.fields['appearance'] = Appearance()
            self.eventDummy.fields['appearance'].flags = 1<<8
            self.eventDummy.fields['appearance'].scale.Set(0.0, 0.0, 0.0)
            self.eventDummy.fields['equipment'] = Equipment()
            lamp = Item(itemType = 24, rarity=3)
            self.eventDummy.fields['equipment'].light = lamp
            self.eventDummy.fields['creatureFlags'] = 0xFFFF
            

        radius_ents = 10
        for i in range(radius_ents):
            radius = UpdateCreature(GetGUID())
            radius.fields['hostility'] = 2
            radius.fields['creatureType'] = 136
            radius.fields['appearance'] = Appearance()
            radius.fields['appearance'].scale.Set(1.0, 0.0, 0.0) 
            radius.fields['appearance'].bodyModel = 2475
            radius.fields['appearance'].headScale = 0.0
            radius.fields['appearance'].handScale = 0.0
            radius.fields['appearance'].footScale = 0.0
            radius.fields['appearance'].shoulder2Scale = 0.0
            radius.fields['appearance'].weaponScale = 0.0
            radius.fields['appearance'].tailScale = 0.0
            radius.fields['appearance'].shoulderScale = 0.0
            radius.fields['appearance'].wingScale = 0.0
            radius.fields['appearance'].bodyOffset.Set(0.0, 5.0, 10.0)
            radius.fields['equipment'] = Equipment()
            radius.fields['level'] = 2**31 -1
            radius.fields['powerBase'] = 0
            radius.fields['name'] = 'King ofthe Hill'
            radius.fields['position'] = self.eventEntity.fields['position'].Copy()
            radius.fields['physicsFlags'] = 17
            radius.fields['HP'] = 10000000000

            r = math.pi * 2 / radius_ents * i
            x = math.sqrt(self.proximity_radius) * math.sin(r)
            y = math.sqrt(self.proximity_radius) * math.cos(r)
            radius.fields['position'] = LongVector3(int(x), int(y), 65536*5) + self.eventEntity.fields['position']
            self.radii.append(radius)
            

        for player in self.players:
            Thread(target=player.SendEventEntityUpdate).start()
            Thread(target=player.SendRadiusUpdate).start()
            Thread(target=player.SendDummyUpdate).start()


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

        for hit in serverupdate.hits:
            killers = [x for x in self.players if x.guid == hit.attackerID]
            killeds = [x for x in self.players if x.guid == hit.targetID]
            if killers and killeds:
                killer = killers[0]
                killed = killeds[0]
                if hit.dmg >= killed.fields['HP'] and not killed.dead:
                    killed.dead = True
                    killer.OnKill(killed)
##                else:
##                    print(hit.dmg, killed.fields['HP'], killed.dead)
        return MODIFY

    def DoProximityCheck(self):
        bad_items = []
        for player in self.playersInProximity:
            if player not in self.players:
                bad_items.append(player)

        for player in bad_items:
            self.playersInProximity.remove(player)

        for player in self.players:
            if 'position' not in player.fields: continue
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


    def GrantXPAndGold(self):
        if len(self.playersInProximity) == 0:
            return

        for player in self.playersInProximity:
            xp = self.XPPerTick
            if player.guid == self.king.guid:
                xp += self.kingXPBonus
                player.AddPoints(self.kingPointsPerTick)
            else:
                player.AddPoints(self.pointsPerTick)

            self.GiveXP(player, xp)

            if player.rewardPoints > self.rewardPoints:
                player.rewardPoints -= self.rewardPoints
                message = f"{player.fields['name']} has reached {self.rewardPoints} points, and receives an additional reward!"
                print(message)
                chat = ChatPacket(message, self.chatGUID)
                for p in self.players:
                    Thread(target=chat.Send, args=[p.connection, False]).start()

                item = self.GenerateItem(player)
                player.GiveItem(item)

        self.DropGold(self.copperPerTick)


    def DropGold(self, amount):
        for material, coinScale in ((11, 10000), (12, 100), (10, 1)):
            item = Item()
            item.itemType = 12 #coin
            item.subType = 0
            item.level = int(float(amount) / coinScale)
            item.material = material
            amount = int(math.fmod(amount, coinScale))
            self.DropItem(item)

    def DropItem(self, item): pass
##        position = self.eventLocation.Copy()
##
##        d = random.uniform(0, 1) * math.pi * 2
##        r = math.sqrt(random.uniform(0, 1)) * self.itemDropRadius
##        position.x += int(math.cos(d) * r)
##        position.y += int(math.sin(d) * r)
##
##        drop = Drop()
##        drop.item = item
##        drop.scale = 1.0
##        drop.position = position
##
##        zoneX, zoneY = drop.position.x // ZONE_SCALE, drop.position.y // ZONE_SCALE
##
##        zoneItems = {(zoneX, zoneY):[drop]}
##
##        update = ServerUpdatePacket()
##        update.zoneItems = zoneItems
##
##        for player in self.players:
##            print('Dropping', drop)
##            Thread(target=update.Send, args=[player.connection, False]).start()



    def GiveXP(self, player, amount):
        if not self.eventDummy:
            return

        # don't give XP to max levels
        if self.maxLevel != 0 and player.entity.level >= self.maxLevel:
            return

        update = ServerUpdatePacket()
        action = Kill()
        action.killer = player.guid
        action.killed = self.eventDummy.guid
        action.XP = amount
        update.kills.append(action)
        Thread(target=update.Send, args=[player.connection, False]).start()

    def GenerateItem(self, entity):
        item_bias = random.randint(0, 100)

        if item_bias < 30:
            item = self.RandomItem(REWARD_WEAPONS)
        elif item_bias < 60:
            item = self.RandomItem(REWARD_ARMOR)
        elif item_bias < 95:
            item = self.RandomItem(REWARD_MISC)
        else:
            item = self.RandomItem(REWARD_PET_ITEMS)

        if item.itemType == 11:
            item.rarity = 2
        elif item.itemType == 20 or item.itemType == 19:
            item.rarity = 0
        else:
            item.rarity = random.randint(3, 4)

        if item.itemType == 19 or item.itemType == 11:
            item.modifier = 0
        else:
            item.modifier = random.randint(0, 16777216)

        if item.itemType == 20:
            item.level = 1
        else:
            item.level = entity.fields['level']

        return item


    def RandomItem(self, itemdict):
        items = list(itemdict.keys())
        item_key = items[random.randint(0, len(items) - 1)]
        item = Item()
        item.itemType = item_key[0]
        item.subType = item_key[1]
        materials = itemdict[item_key]
        item.material = materials[random.randint(0, len(materials) - 1)]
        return item

    def AnnounceJoin(self, name):
        message = f'{name} has joined.'
        chat = ChatPacket(message, self.chatGUID)
        for player in self.players:
            Thread(target=chat.Send, args=[player.connection, False]).start()
             
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
        if 'HP' in packet.fields:
            if packet.fields['HP'] > 0.0:
                player.dead = False

        if 'name' in packet.fields:
            koth.AnnounceJoin(packet.fields['name'])
                
        if player.new:
            player.new = False
            player.SendEventEntityUpdate()
            player.SendRadiusUpdate()
            player.SendDummyUpdate()
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
    player.SendDummyUpdate(False)

def HandleServerUpdate(connection, packet, fromClient):
    koth.Update(packet)
    return MODIFY
    
