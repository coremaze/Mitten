import struct
import io
from CubeTypes import LongVector3
from CubeTypes import FloatVector3
from CubeTypes import Appearance
from CubeTypes import IntVector3
from CubeTypes import Item
class Creature():
    size = 0x1168
    def __init__(self, position, orientation, velocity, acceleration, retreat, headRotation, physicsFlags, hostility,
                 creatureType, mode, modeTimer, combo, lastHitTime, appearance, creatureFlags, rollTime, stunTime,
                 slowedTime, iceEffectTime, windEffectTime, showPatchTime, classType, specialization, chargedMP, unkIntVec1,
                 unkIntVec2, rayHit, HP, MP, blockPower, HPMultiplier, attackSpeedMultiplier, damageMultiplier, armorMultiplier,
                 resistanceMultiplier, unkByte1, unkByte2, level, XP, parentOwner, unkLong1, powerBase, unkInt1, unkInt2,
                 spawnPosition, unkIntVec3, unkByte3, consumable, equipment1, equipment2, equipment3, equipment4, equipment5,
                 equipment6, equipment7 , equipment8 , equipment9 , equipment10, equipment11, equipment12, equipment13,
                 name, skill1, skill2, skill3, skill4, skill5, skill6, skill7, skill8, skill9, skill10, skill11, manaCubes):
        self.position = position
        self.orientation = orientation
        self.velocity = velocity
        self.acceleration = acceleration
        self.retreat = retreat
        self.headRotation = headRotation
        self.physicsFlags = physicsFlags
        self.hostility = hostility
        self.creatureType = creatureType
        self.mode = mode
        self.modeTimer = modeTimer
        self.combo = combo
        self.lastHitTime = lastHitTime
        self.appearance = appearance
        self.creatureFlags = creatureFlags
        self.rollTime = rollTime
        self.stunTime = stunTime
        self.slowedTime = slowedTime
        self.iceEffectTime = iceEffectTime
        self.windEffectTime = windEffectTime
        self.showPatchTime = showPatchTime
        self.classType = classType
        self.specialization = specialization
        self.chargedMP = chargedMP
        self.unkIntVec1 = unkIntVec1
        self.unkIntVec2 = unkIntVec2
        self.rayHit = rayHit
        self.HP = HP
        self.MP = MP
        self.blockPower = blockPower
        self.HPMultiplier = HPMultiplier
        self.attackSpeedMultiplier = attackSpeedMultiplier
        self.damageMultiplier = damageMultiplier
        self.armorMultiplier = armorMultiplier
        self.resistanceMultiplier = resistanceMultiplier
        self.unkByte1 = unkByte1
        self.unkByte2 = unkByte2
        self.level = level
        self.XP = XP
        self.parentOwner = parentOwner
        self.unkLong1 = unkLong1
        self.powerBase = powerBase
        self.unkInt1 = unkInt1
        self.unkInt2 = unkInt2
        self.spawnPosition = spawnPosition
        self.unkIntVec3 = unkIntVec3
        self.unkByte3 = unkByte3
        self.consumable = consumable
        self.equipment1 = equipment1
        self.equipment2 = equipment2
        self.equipment3 = equipment3
        self.equipment4 = equipment4
        self.equipment5 = equipment5
        self.equipment6 = equipment6
        self.equipment7 = equipment7
        self.equipment8 = equipment8
        self.equipment9 = equipment9
        self.equipment10 = equipment10
        self.equipment11 = equipment11
        self.equipment12 = equipment12
        self.equipment13 = equipment13
        self.name = name
        self.skill1 = skill1
        self.skill2 = skill2
        self.skill3 = skill3
        self.skill4 = skill4
        self.skill5 = skill5
        self.skill6 = skill6
        self.skill7 = skill7
        self.skill8 = skill8
        self.skill9 = skill9
        self.skill10 = skill10
        self.skill11 = skill11
        self.manaCubes = manaCubes

    @classmethod
    def Import(data):
        position = LongVector3.Import(data)
        orientation = FloatVector3.Import(data)
        velocity = FloatVector3.Import(data)
        acceleration = FloatVector3.Import(data)
        retreat = FloatVector3.Import(data)
        headRotation, = struct.unpack('<f', data.read(4))
        physicsFlags, = struct.unpack('<I', data.read(4))
        hostility, = struct.unpack('<B', data.read(1))
        creatureType, = struct.unpack('<i', data.read(4))
        mode, = struct.unpack('<B', data.read(1))
        modeTimer, = struct.unpack('<i', data.read(4))
        combo, = struct.unpack('<i', data.read(4))
        lastHitTime, = struct.unpack('<i', data.read(4))
        appearance = Appearance.Import(data)
        creatureFlags, = struct.unpack('<H', data.read(2))
        rollTime, = struct.unpack('<i', data.read(4))
        stunTime, = struct.unpack('<i', data.read(4))
        slowedTime, = struct.unpack('<i', data.read(4))
        iceEffectTime, = struct.unpack('<i', data.read(4))
        windEffectTime, = struct.unpack('<i', data.read(4))
        showPatchTime, = struct.unpack('<f', data.read(4))
        classType, = struct.unpack('<B', data.read(1))
        specialization, = struct.unpack('<B', data.read(1))
        chargedMP, = struct.unpack('<f', data.read(4))
        unkIntVec1 = IntVector3.Import(data)
        unkIntVec2 = IntVector3.Import(data)
        rayHit = FloatVector3.Import(data)
        HP, = struct.unpack('<f', data.read(4))
        MP, = struct.unpack('<f', data.read(4))
        blockPower, = struct.unpack('<f', data.read(4))
        HPMultiplier, = struct.unpack('<f', data.read(4))
        attackSpeedMultiplier, = struct.unpack('<f', data.read(4))
        damageMultiplier, = struct.unpack('<f', data.read(4))
        armorMultiplier, = struct.unpack('<f', data.read(4))
        resistanceMultiplier, = struct.unpack('<f', data.read(4))
        unkByte1, = struct.unpack('<B', data.read(1))
        unkByte2, = struct.unpack('<B', data.read(1))
        level, = struct.unpack('<i', data.read(4))
        XP, = struct.unpack('<i', data.read(4))
        parentOwner, = struct.unpack('<q', data.read(8))
        unkLong1, = struct.unpack('<q', data.read(8))
        powerBase, = struct.unpack('<B', data.read(1))
        unkInt1, = struct.unpack('<i', data.read(4))
        unkInt2, = struct.unpack('<i', data.read(4))
        spawnPosition = LongVector3.Import(data)
        unkIntVec3, = IntVector3.Import(data)
        unkByte3, = struct.unpack('<B', data.read(1))
        consumable = Item.Import(data)
        equipment1 = Item.Import(data)
        equipment2 = Item.Import(data)
        equipment3 = Item.Import(data)
        equipment4 = Item.Import(data)
        equipment5 = Item.Import(data)
        equipment6 = Item.Import(data)
        equipment7 = Item.Import(data)
        equipment8 = Item.Import(data)
        equipment9 = Item.Import(data)
        equipment10 = Item.Import(data)
        equipment11 = Item.Import(data)
        equipment12 = Item.Import(data)
        equipment13 = Item.Import(data)
        name = data.read(16).decode('utf-16le')
        manaCubes, = struct.unpack('<i', data.read(4))
        return Creature(position, orientation, velocity, acceleration, retreat, headRotation, physicsFlags, hostility,
                 creatureType, mode, modeTimer, combo, lastHitTime, appearance, creatureFlags, rollTime, stunTime,
                 slowedTime, iceEffectTime, windEffectTime, showPatchTime, classType, specialization, chargedMP, unkIntVec1,
                 unkIntVec2, rayHit, HP, MP, blockPower, HPMultiplier, attackSpeedMultiplier, damageMultiplier, armorMultiplier,
                 resistanceMultiplier, unkByte1, unkByte2, level, XP, parentOwner, unkLong1, powerBase, unkInt1, unkInt2,
                 spawnPosition, unkIntVec3, unkByte3, consumable, equipment1, equipment2, equipment3, equipment4, equipment5,
                 equipment6, equipment7 , equipment8 , equipment9 , equipment10, equipment11, equipment12, equipment13,
                 name, skill1, skill2, skill3, skill4, skill5, skill6, skill7, skill8, skill9, skill10, skill11, manaCubes)


    def Export(self):
        return packet
    

