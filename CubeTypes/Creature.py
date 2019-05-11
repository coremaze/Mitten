import struct
import io
from CubeTypes import LongVector3
from CubeTypes import FloatVector3

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
        position = LongVector3.Import(data.read(LongVector3.size))
        orientation = FloatVector3.Import(data.read(FloatVector3.size))
        velocity = FloatVector3.Import(data.read(FloatVector3.size))
        acceleration = FloatVector3.Import(data.read(FloatVector3.size))
        retreat = FloatVector3.Import(data.read(FloatVector3.size))
        headRotation = struct.unpack('<f', data.read(4))
        physicsFlags = struct.unpack('<I', data.read(4))
        hostility = struct.unpack('<B', data.read(1))
        creatureType = struct.unpack('<i', data.read(4))
        mode = struct.unpack('<B', data.read(1))
        modeTimer = struct.unpack('<i', data.read(4))
        combo = struct.unpack('<i', data.read(4))
        lastHitTime = struct.unpack('<i', data.read(4))
        #not complete


    def Export(self):
        return packet
    

