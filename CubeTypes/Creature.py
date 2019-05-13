import struct
import io
from CubeTypes.LongVector3 import LongVector3
from CubeTypes.FloatVector3 import FloatVector3
from CubeTypes.Appearance import Appearance
from CubeTypes.IntVector3 import IntVector3
from CubeTypes.Item import Item
class Creature():
    size = 0x1168
    def __init__(self, position, orientation, velocity, acceleration, retreat, headRotation, physicsFlags, hostility,
                 unusedByte1, unusedByte2, unusedByte3, creatureType, mode, unusedByte4, unusedByte5, unusedByte6,
                 modeTimer, combo, lastHitTime, appearance, creatureFlags, unusedByte7, unusedByte8, rollTime, stunTime,
                 slowedTime, iceEffectTime, windEffectTime, showPatchTime, classType, specialization, unusedByte9,
                 unusedByte10, chargedMP, unkIntVec1, unkIntVec2, rayHit, HP, MP, blockPower, HPMultiplier, attackSpeedMultiplier,
                 damageMultiplier, armorMultiplier, resistanceMultiplier, unkByte1, unkByte2, unusedByte11, unusedByte12,
                 level, XP, parentOwner, unkLong1, powerBase, unusedByte13, unusedByte14, unusedByte15, unkInt1, superWeird,
                 unkInt2, spawnPosition, unkIntVec3, unkByte3, unusedByte16, unusedByte17, unusedByte18, consumable, equipment1,
                 equipment2, equipment3, equipment4, equipment5, equipment6, equipment7, equipment8, equipment9, equipment10,
                 equipment11, equipment12, equipment13, skill1, skill2, skill3, skill4, skill5, skill6, skill7, skill8, skill9,
                 skill10, skill11, manaCubes, name):
        self.position = position
        self.orientation = orientation
        self.velocity = velocity
        self.acceleration = acceleration
        self.retreat = retreat
        self.headRotation = headRotation
        self.physicsFlags = physicsFlags
        self.hostility = hostility
        self.unusedByte1 = unusedByte1
        self.unusedByte2 = unusedByte2
        self.unusedByte3 = unusedByte3
        self.creatureType = creatureType
        self.mode = mode
        self.unusedByte4 = unusedByte4
        self.unusedByte5 = unusedByte5
        self.unusedByte6 = unusedByte6
        self.modeTimer = modeTimer
        self.combo = combo
        self.lastHitTime = lastHitTime
        self.appearance = appearance
        self.creatureFlags = creatureFlags
        self.unusedByte7 = unusedByte7
        self.unusedByte8 = unusedByte8
        self.rollTime = rollTime
        self.stunTime = stunTime
        self.slowedTime = slowedTime
        self.iceEffectTime = iceEffectTime
        self.windEffectTime = windEffectTime
        self.showPatchTime = showPatchTime
        self.classType = classType
        self.specialization = specialization
        self.unusedByte9 = unusedByte9
        self.unusedByte10 = unusedByte10
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
        self.unusedByte11 = unusedByte11
        self.unusedByte12 = unusedByte12
        self.level = level
        self.XP = XP
        self.parentOwner = parentOwner
        self.unkLong1 = unkLong1
        self.powerBase = powerBase
        self.unusedByte13 = unusedByte13
        self.unusedByte14 = unusedByte14
        self.unusedByte15 = unusedByte15
        self.unkInt1 = unkInt1
        self.superWeird = superWeird
        self.unkInt2 = unkInt2
        self.spawnPosition = spawnPosition
        self.unkIntVec3 = unkIntVec3
        self.unkByte3 = unkByte3
        self.unusedByte16 = unusedByte16
        self.unusedByte17 = unusedByte17
        self.unusedByte18 = unusedByte18
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
        self.name = name

    @classmethod
    def Import(self, data):      
        position = LongVector3.Import(data)
        orientation = FloatVector3.Import(data)
        velocity = FloatVector3.Import(data)
        acceleration = FloatVector3.Import(data)
        retreat = FloatVector3.Import(data)
        headRotation, = struct.unpack('<f', data.read(4))
        physicsFlags, = struct.unpack('<I', data.read(4))
        hostility, = struct.unpack('<B', data.read(1))
        unusedByte1, = struct.unpack('<B', data.read(1))
        unusedByte2, = struct.unpack('<B', data.read(1))
        unusedByte3, = struct.unpack('<B', data.read(1))
        creatureType, = struct.unpack('<I', data.read(4))
        mode, = struct.unpack('<B', data.read(1))
        unusedByte4, = struct.unpack('<B', data.read(1))
        unusedByte5, = struct.unpack('<B', data.read(1))
        unusedByte6, = struct.unpack('<B', data.read(1))
        modeTimer, = struct.unpack('<i', data.read(4))
        combo, = struct.unpack('<i', data.read(4))
        lastHitTime, = struct.unpack('<i', data.read(4))
        appearance = Appearance.Import(data)
        creatureFlags, = struct.unpack('<H', data.read(2))
        unusedByte7, = struct.unpack('<B', data.read(1))
        unusedByte8, = struct.unpack('<B', data.read(1))
        rollTime, = struct.unpack('<i', data.read(4))
        stunTime, = struct.unpack('<i', data.read(4))
        slowedTime, = struct.unpack('<i', data.read(4))
        iceEffectTime, = struct.unpack('<i', data.read(4))
        windEffectTime, = struct.unpack('<i', data.read(4))
        showPatchTime, = struct.unpack('<f', data.read(4))
        classType, = struct.unpack('<B', data.read(1))
        specialization, = struct.unpack('<B', data.read(1))
        unusedByte9, = struct.unpack('<B', data.read(1))
        unusedByte10, = struct.unpack('<B', data.read(1))
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
        unusedByte11, = struct.unpack('<B', data.read(1))
        unusedByte12, = struct.unpack('<B', data.read(1))
        level, = struct.unpack('<i', data.read(4))
        XP, = struct.unpack('<i', data.read(4))
        parentOwner, = struct.unpack('<q', data.read(8))
        unkLong1, = struct.unpack('<q', data.read(8))
        powerBase, = struct.unpack('<B', data.read(1))
        unusedByte13, = struct.unpack('<B', data.read(1))
        unusedByte14, = struct.unpack('<B', data.read(1))
        unusedByte15, = struct.unpack('<B', data.read(1))
        unkInt1, = struct.unpack('<i', data.read(4))
        superWeird = IntVector3.Import(data)
        unkInt2, = struct.unpack('<i', data.read(4))
        spawnPosition = LongVector3.Import(data)
        unkIntVec3 = IntVector3.Import(data)
        unkByte3, = struct.unpack('<B', data.read(1))
        unusedByte16, = struct.unpack('<B', data.read(1))
        unusedByte17, = struct.unpack('<B', data.read(1))
        unusedByte18, = struct.unpack('<B', data.read(1))
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
        skill1, = struct.unpack('<i', data.read(4))
        skill2, = struct.unpack('<i', data.read(4))
        skill3, = struct.unpack('<i', data.read(4))
        skill4, = struct.unpack('<i', data.read(4))
        skill5, = struct.unpack('<i', data.read(4))
        skill6, = struct.unpack('<i', data.read(4))
        skill7, = struct.unpack('<i', data.read(4))
        skill8, = struct.unpack('<i', data.read(4))
        skill9, = struct.unpack('<i', data.read(4))
        skill10, = struct.unpack('<i', data.read(4))
        skill11, = struct.unpack('<i', data.read(4))
        manaCubes, = struct.unpack('<i', data.read(4))
        name = ''.join([chr(x) for x in data.read(16).rstrip(b'\x00')]) #this method might be slightly more resilient than a decoder
        return Creature(position, orientation, velocity, acceleration, retreat, headRotation, physicsFlags, hostility,
                 unusedByte1, unusedByte2, unusedByte3, creatureType, mode, unusedByte4, unusedByte5, unusedByte6,
                 modeTimer, combo, lastHitTime, appearance, creatureFlags, unusedByte7, unusedByte8, rollTime, stunTime,
                 slowedTime, iceEffectTime, windEffectTime, showPatchTime, classType, specialization, unusedByte9,
                 unusedByte10, chargedMP, unkIntVec1, unkIntVec2, rayHit, HP, MP, blockPower, HPMultiplier, attackSpeedMultiplier,
                 damageMultiplier, armorMultiplier, resistanceMultiplier, unkByte1, unkByte2, unusedByte11, unusedByte12,
                 level, XP, parentOwner, unkLong1, powerBase, unusedByte13, unusedByte14, unusedByte15, unkInt1, superWeird,
                 unkInt2, spawnPosition, unkIntVec3, unkByte3, unusedByte16, unusedByte17, unusedByte18, consumable, equipment1,
                 equipment2, equipment3, equipment4, equipment5, equipment6, equipment7, equipment8, equipment9, equipment10,
                 equipment11, equipment12, equipment13, skill1, skill2, skill3, skill4, skill5, skill6, skill7, skill8, skill9,
                 skill10, skill11, manaCubes, name)


    def Export(self):
        dataList = []
        dataList.append(self.position.Export())
        dataList.append(self.orientation.Export())
        dataList.append(self.velocity.Export())
        dataList.append(self.acceleration.Export())
        dataList.append(self.retreat.Export())
        dataList.append(struct.pack('<f', self.headRotation))
        dataList.append(struct.pack('<I', self.physicsFlags))
        dataList.append(struct.pack('<B', self.hostility))
        dataList.append(struct.pack('<B', self.unusedByte1))
        dataList.append(struct.pack('<B', self.unusedByte2))
        dataList.append(struct.pack('<B', self.unusedByte3))
        dataList.append(struct.pack('<I', self.creatureType))
        dataList.append(struct.pack('<B', self.mode))
        dataList.append(struct.pack('<B', self.unusedByte4))
        dataList.append(struct.pack('<B', self.unusedByte5))
        dataList.append(struct.pack('<B', self.unusedByte6))
        dataList.append(struct.pack('<i', self.modeTimer))
        dataList.append(struct.pack('<i', self.combo))
        dataList.append(struct.pack('<i', self.lastHitTime))
        dataList.append(self.appearance.Export())
        dataList.append(struct.pack('<H', self.creatureFlags))
        dataList.append(struct.pack('<B', self.unusedByte7))
        dataList.append(struct.pack('<B', self.unusedByte8))
        dataList.append(struct.pack('<i', self.rollTime))
        dataList.append(struct.pack('<i', self.stunTime))
        dataList.append(struct.pack('<i', self.slowedTime))
        dataList.append(struct.pack('<i', self.iceEffectTime))
        dataList.append(struct.pack('<i', self.windEffectTime))
        dataList.append(struct.pack('<f', self.showPatchTime))
        dataList.append(struct.pack('<B', self.classType))
        dataList.append(struct.pack('<B', self.specialization))
        dataList.append(struct.pack('<B', self.unusedByte9))
        dataList.append(struct.pack('<B', self.unusedByte10))
        dataList.append(struct.pack('<f', self.chargedMP))
        dataList.append(self.unkIntVec1.Export())
        dataList.append(self.unkIntVec2.Export())
        dataList.append(self.rayHit.Export())
        dataList.append(struct.pack('<f', self.HP))
        dataList.append(struct.pack('<f', self.MP))
        dataList.append(struct.pack('<f', self.blockPower))
        dataList.append(struct.pack('<f', self.HPMultiplier))
        dataList.append(struct.pack('<f', self.attackSpeedMultiplier))
        dataList.append(struct.pack('<f', self.damageMultiplier))
        dataList.append(struct.pack('<f', self.armorMultiplier))
        dataList.append(struct.pack('<f', self.resistanceMultiplier))
        dataList.append(struct.pack('<B', self.unkByte1))
        dataList.append(struct.pack('<B', self.unkByte2))
        dataList.append(struct.pack('<B', self.unusedByte11))
        dataList.append(struct.pack('<B', self.unusedByte12))
        dataList.append(struct.pack('<i', self.level))
        dataList.append(struct.pack('<i', self.XP))
        dataList.append(struct.pack('<q', self.parentOwner))
        dataList.append(struct.pack('<q', self.unkLong1))
        dataList.append(struct.pack('<B', self.powerBase))
        dataList.append(struct.pack('<B', self.unusedByte13))
        dataList.append(struct.pack('<B', self.unusedByte14))
        dataList.append(struct.pack('<B', self.unusedByte15))
        dataList.append(struct.pack('<i', self.unkInt1))
        dataList.append(self.superWeird.Export())
        dataList.append(struct.pack('<i', self.unkInt2))
        dataList.append(self.spawnPosition.Export())
        dataList.append(self.unkIntVec3.Export())
        dataList.append(struct.pack('<B', self.unkByte3))
        dataList.append(struct.pack('<B', self.unusedByte16))
        dataList.append(struct.pack('<B', self.unusedByte17))
        dataList.append(struct.pack('<B', self.unusedByte18))
        dataList.append(self.consumable.Export())
        dataList.append(self.equipment1.Export())
        dataList.append(self.equipment2.Export())
        dataList.append(self.equipment3.Export())
        dataList.append(self.equipment4.Export())
        dataList.append(self.equipment5.Export())
        dataList.append(self.equipment6.Export())
        dataList.append(self.equipment7.Export())
        dataList.append(self.equipment8.Export())
        dataList.append(self.equipment9.Export())
        dataList.append(self.equipment10.Export())
        dataList.append(self.equipment11.Export())
        dataList.append(self.equipment12.Export())
        dataList.append(self.equipment13.Export())
        dataList.append(struct.pack('<i', self.skill1))
        dataList.append(struct.pack('<i', self.skill2))
        dataList.append(struct.pack('<i', self.skill3))
        dataList.append(struct.pack('<i', self.skill4))
        dataList.append(struct.pack('<i', self.skill5))
        dataList.append(struct.pack('<i', self.skill6))
        dataList.append(struct.pack('<i', self.skill7))
        dataList.append(struct.pack('<i', self.skill8))
        dataList.append(struct.pack('<i', self.skill9))
        dataList.append(struct.pack('<i', self.skill10))
        dataList.append(struct.pack('<i', self.skill11))
        dataList.append(struct.pack('<i', self.manaCubes))
        dataList.append(bytes([ord(x)&0xFF for x in self.name]) + b'\x00'*(16-len(self.name)))
        return b''.join(dataList)
    

