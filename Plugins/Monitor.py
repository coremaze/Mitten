# Imports
from Packets.EntityUpdatePacket import EntityUpdatePacket
from Packets.AirTrafficPacket import AirTrafficPacket
from Packets.TimePacket import TimePacket
from Packets.EntityUpdateFinishedPacket import EntityUpdateFinishedPacket
from Packets.ServerUpdatePacket import ServerUpdatePacket
from Packets.BuildingModPacket import BuildingModZoneLoadPacket, BuildingModZoneUnloadPacket
from Packets.RegionDiscoveredPacket import RegionDiscoveredPacket
from Packets.ZoneDiscoveredPacket import ZoneDiscoveredPacket
from Packets.ShootPacket import ShootPacket
from Packets.ActionPacket import ActionPacket
from Packets.HitPacket import HitPacket
from Packets.JoinPacket import JoinPacket
from Mitten.Constants import *


from CubeTypes import *
import json

# Variable Definitions

aConnections = []
aHandlers = {}

ITEM_NAMES = {
    (1, 0): 'Cookie',
    (1, 1): 'LifePotion',
    (1, 2): 'CactusPotion',
    (1, 3): 'ManaPotion',
    (1, 4): 'GinsengSoup',
    (1, 5): 'SnowBerryMash',
    (1, 6): 'MushroomSpit',
    (1, 7): 'Bomb',
    (1, 8): 'PineappleSlice',
    (1, 9): 'PumpkinMuffin',
    (2, 0): 'Formula',
    (3, 0): 'Sword',
    (3, 1): 'Axe',
    (3, 2): 'Mace',
    (3, 3): 'Dagger',
    (3, 4): 'Fist',
    (3, 5): 'Longsword',
    (3, 6): 'Bow',
    (3, 7): 'Crossbow',
    (3, 8): 'Boomerang',
    (3, 9): 'Arrow',
    (3, 10): 'Staff',
    (3, 11): 'Wand',
    (3, 12): 'Bracelet',
    (3, 13): 'Shield',
    (3, 14): 'Arrows',
    (3, 15): 'Greatsword',
    (3, 16): 'Greataxe',
    (3, 17): 'Greatmace',
    (3, 20): 'Torch',
    (4, 0): 'ChestArmor',
    (5, 0): 'Gloves',
    (6, 0): 'Boots',
    (7, 0): 'ShoulderArmor',
    (8, 0): 'Amulet',
    (9, 0): 'Ring',
    (11, 0): 'Nugget',
    (11, 1): 'Log',
    (11, 2): 'Feather',
    (11, 3): 'Horn',
    (11, 4): 'Claw',
    (11, 5): 'Fiber',
    (11, 6): 'Cobweb',
    (11, 7): 'Hair',
    (11, 8): 'Crystal',
    (11, 9): 'Yarn',
    (11, 10): 'Cube',
    (11, 11): 'Capsule',
    (11, 12): 'Flask',
    (11, 13): 'Orb',
    (11, 14): 'Spirit',
    (11, 15): 'Mushroom',
    (11, 16): 'Pumpkin',
    (11, 17): 'Pineapple',
    (11, 18): 'RadishSlice',
    (11, 19): 'ShimmerMushroom',
    (11, 20): 'GinsengRoot',
    (11, 21): 'OnionSlice',
    (11, 22): 'Heartflower',
    (11, 23): 'PricklyPear',
    (11, 24): 'FrozenHeartflower',
    (11, 25): 'Soulflower',
    (11, 26): 'WaterFlask',
    (11, 27): 'SnowBerry',
    (12, 0): 'Coin',
    (13, 0): 'PlatinumCoin',
    (14, 0): 'Leftovers',
    (15, 0): 'Beak',
    (16, 0): 'Painting',
    (18, 0): 'Candle',
    (18, 1): 'Candle',
    (19, 0): 'Pet',
    (20, 0): 'Bait',
    (20, 1): 'Bait',
    (20, 2): 'Bait',
    (20, 3): 'Bait',
    (20, 4): 'Bait',
    (20, 5): 'Bait',
    (20, 6): 'Bait',
    (20, 7): 'Bait',
    (20, 8): 'Bait',
    (20, 9): 'Bait',
    (20, 10): 'Bait',
    (20, 11): 'Bait',
    (20, 12): 'Bait',
    (20, 13): 'Bait',
    (20, 14): 'Bait',
    (20, 15): 'Bait',
    (20, 16): 'Bait',
    (20, 17): 'Bait',
    (20, 18): 'Bait',
    (20, 19): 'BubbleGum',
    (20, 20): 'Bait',
    (20, 21): 'Bait',
    (20, 22): 'VanillaCupcake',
    (20, 23): 'ChocolateCupcake',
    (20, 24): 'Bait',
    (20, 25): 'CinnamonRole',
    (20, 26): 'Waffle',
    (20, 27): 'Croissant',
    (20, 28): 'Bait',
    (20, 29): 'Bait',
    (20, 30): 'Candy',
    (20, 31): 'Bait',
    (20, 32): 'Bait',
    (20, 33): 'PumpkinMash',
    (20, 34): 'CottonCandy',
    (20, 35): 'Carrot',
    (20, 36): 'BlackberryMarmelade',
    (20, 37): 'GreenJelly',
    (20, 38): 'PinkJelly',
    (20, 39): 'YellowJelly',
    (20, 40): 'BlueJelly',
    (20, 41): 'Bait',
    (20, 42): 'Bait',
    (20, 43): 'Bait',
    (20, 44): 'Bait',
    (20, 45): 'Bait',
    (20, 46): 'Bait',
    (20, 47): 'Bait',
    (20, 48): 'Bait',
    (20, 49): 'Bait',
    (20, 50): 'BananaSplit',
    (20, 51): 'Bait',
    (20, 52): 'Bait',
    (20, 53): 'Popcorn',
    (20, 54): 'Bait',
    (20, 55): 'LicoriceCandy',
    (20, 56): 'CerealBar',
    (20, 57): 'SaltedCaramel',
    (20, 58): 'GingerTartlet',
    (20, 59): 'MangoJuice',
    (20, 60): 'FruitBasket',
    (20, 61): 'MelonIceCream',
    (20, 62): 'BloodOrangeJuice',
    (20, 63): 'MilkChocolateBar',
    (20, 64): 'MintChocolateBar',
    (20, 65): 'WhiteChocolateBar',
    (20, 66): 'CaramelChocolateBar',
    (20, 67): 'ChocolateCookie',
    (20, 68): 'Bait',
    (20, 69): 'Bait',
    (20, 70): 'Bait',
    (20, 71): 'Bait',
    (20, 72): 'Bait',
    (20, 73): 'Bait',
    (20, 74): 'SugarCandy',
    (20, 75): 'AppleRing',
    (20, 76): 'Bait',
    (20, 77): 'Bait',
    (20, 78): 'Bait',
    (20, 79): 'Bait',
    (20, 80): 'Bait',
    (20, 81): 'Bait',
    (20, 82): 'Bait',
    (20, 83): 'Bait',
    (20, 84): 'Bait',
    (20, 85): 'Bait',
    (20, 86): 'WaterIce',
    (20, 87): 'ChocolateDonut',
    (20, 88): 'Pancakes',
    (20, 89): 'Bait',
    (20, 90): 'StrawberryCake',
    (20, 91): 'ChocolateCake',
    (20, 92): 'Lollipop',
    (20, 93): 'Softice',
    (20, 94): 'Bait',
    (20, 95): 'Bait',
    (20, 96): 'Bait',
    (20, 97): 'Bait',
    (20, 98): 'CandiedApple',
    (20, 99): 'DateCookie',
    (20, 100): 'Bait',
    (20, 101): 'Bait',
    (20, 102): 'Bread',
    (20, 103): 'Curry',
    (20, 104): 'Lolly',
    (20, 105): 'LemonTart',
    (20, 106): 'StrawberryCocktail',
    (20, 107): 'Bait',
    (20, 108): 'Bait',
    (20, 109): 'Bait',
    (20, 110): 'Bait',
    (20, 111): 'Bait',
    (20, 112): 'Bait',
    (20, 113): 'Bait',
    (20, 114): 'Bait',
    (20, 115): 'Bait',
    (20, 116): 'Bait',
    (20, 117): 'Bait',
    (20, 118): 'Bait',
    (20, 119): 'Bait',
    (20, 120): 'Bait',
    (20, 121): 'Bait',
    (20, 122): 'Bait',
    (20, 123): 'Bait',
    (20, 124): 'Bait',
    (20, 125): 'Bait',
    (20, 126): 'Bait',
    (20, 127): 'Bait',
    (20, 128): 'Bait',
    (20, 129): 'Bait',
    (20, 130): 'Bait',
    (20, 131): 'Bait',
    (20, 132): 'Bait',
    (20, 133): 'Bait',
    (20, 134): 'Bait',
    (20, 135): 'Bait',
    (20, 136): 'Bait',
    (20, 137): 'Bait',
    (20, 138): 'Bait',
    (20, 139): 'Bait',
    (20, 140): 'Bait',
    (20, 141): 'Bait',
    (20, 142): 'Bait',
    (20, 143): 'Bait',
    (20, 144): 'Bait',
    (20, 145): 'Bait',
    (20, 146): 'Bait',
    (20, 147): 'Bait',
    (20, 148): 'Bait',
    (20, 149): 'Bait',
    (20, 150): 'Bait',
    (20, 151): 'BiscuitRole',
    (20, 152): 'Bait',
    (20, 153): 'Bait',
    (20, 154): 'Bait',
    (20, 155): 'Bait',
    (21, 0): 'Amulet1',
    (21, 1): 'Amulet2',
    (21, 2): 'JewelCase',
    (21, 3): 'Key',
    (21, 4): 'Medicine',
    (21, 5): 'Antivenom',
    (21, 6): 'BandAid',
    (21, 7): 'Crutch',
    (21, 8): 'Bandage',
    (21, 9): 'Salve',
    (23, 0): 'HangGlider',
    (23, 1): 'Boat',
    (24, 0): 'Lamp',
    (25, 0): 'ManaCube'
}

def canDict(obj):
    try:
        somth = obj.__dict__
        return str(somth)
    except:
        return str(obj)

# Function Definitions & Implementations
def BanIP(IP):
    while True:
        try:
            with open('bans.txt', 'a+') as f:
                f.write(f'\n{IP}\n')
        except FileNotFoundError:
            with open('bans.txt', 'w') as f:
                pass
        else:
            break


def HandleJoinPacket(connection, packet, fromClient):
    if connection not in aConnections:
        #aConnections.append(connection)
        pass
    return

def HandleActionPacket(connection, packet, fromClient):
    sPrefix = ["[FROM SERVER]", "[FROM CLIENT]"][fromClient]
    print(f'{sPrefix} {json.dumps( {type(packet).__name__: packet.__dict__}, default=canDict  )}')
    if packet.interactionType is not 6: return
    if ITEM_NAMES.get((packet.item.itemType, packet.item.subType)) is not 'Bait': return
    BanIP(connection.ClientIP())
    print(f'[!] BANNED {connection.ClientIP()} from server.')
    connection.Close()
    return BLOCK

def HandleGenericPacket(connection, packet, fromClient):
    if type(packet) in ( EntityUpdatePacket, EntityUpdateFinishedPacket ):
        return
    if not fromClient: return
    sPrefix = ["[FROM SERVER]", "[FROM CLIENT]"][fromClient]
    print(f'{sPrefix} {json.dumps( {type(packet).__name__: packet.__dict__}, default=canDict  )}')


                                                    
# Packet event - called every time a packet is received.                                                   
def HandlePacket(connection, packet, fromClient):
    return aHandlers.get(type(packet).pID, HandleGenericPacket)(connection, packet, fromClient)
    
# Variable Implementations
#aHandlers[JoinPacket.pID] = HandleJoinPacket
aHandlers[ActionPacket.pID] = HandleActionPacket
    

