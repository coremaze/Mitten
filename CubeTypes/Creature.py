import struct
import io
from CubeTypes.LongVector3 import LongVector3
from CubeTypes.FloatVector3 import FloatVector3
from CubeTypes.Appearance import Appearance
from CubeTypes.IntVector3 import IntVector3
from CubeTypes.Item import Item
from CubeTypes.Equipment import Equipment
from CubeTypes.StatMultipliers import StatMultipliers
class Creature():
    size = 0x1168
    def __init__(self,
                 position = None,
                 orientation = None,
                 velocity = None,
                 acceleration = None,
                 retreat = None,
                 headRotation = 0.0,
                 physicsFlags = 0,
                 hostility = 0,
                 unusedByte1 = 0,
                 unusedByte2 = 0,
                 unusedByte3 = 0,
                 creatureType = 0,
                 mode = 0,
                 unusedByte4 = 0,
                 unusedByte5 = 0,
                 unusedByte6 = 0,
                 modeTimer = 0,
                 combo = 0,
                 lastHitTime = 0,
                 appearance = None,
                 creatureFlags = 0,
                 unusedByte7 = 0,
                 unusedByte8 = 0,
                 rollTime = 0,
                 stunTime = 0,
                 slowedTime = 0,
                 iceEffectTime = 0,
                 windEffectTime = 0,
                 showPatchTime = 0,
                 classType = 0,
                 specialization = 0,
                 unusedByte9 = 0,
                 unusedByte10 = 0,
                 chargedMP = 0.0,
                 unkIntVec1 = None,
                 unkIntVec2 = None,
                 rayHit = None,
                 HP = 0.0,
                 MP = 0.0,
                 blockPower = 0.0,
                 statMultipliers = None,
                 unkByte1 = 0,
                 unkByte2 = 0,
                 unusedByte11 = 0,
                 unusedByte12 = 0,
                 level = 0,
                 XP = 0,
                 parentOwner = 0,
                 unkLong1 = 0,
                 powerBase = 0,
                 unusedByte13 = 0,
                 unusedByte14 = 0,
                 unusedByte15 = 0,
                 unkInt1 = 0,
                 superWeird = None,
                 unkInt2 = 0,
                 spawnPosition = None,
                 unkIntVec3 = None,
                 unkByte3 = 0,
                 unusedByte16 = 0,
                 unusedByte17 = 0,
                 unusedByte18 = 0,
                 consumable = None,
                 equipment = None,
                 skills = [0]*11,
                 manaCubes = 0,
                 name = ''):

        if position is None: position = LongVector3()
        if orientation is None: orientation = FloatVector3()
        if velocity is None: velocity = FloatVector3()
        if acceleration is None: acceleration = FloatVector3()
        if retreat is None: retreat = FloatVector3()
        if appearance is None: appearance = Appearance()
        if unkIntVec1 is None: unkIntVec1 = IntVector3()
        if unkIntVec2 is None: unkIntVec2 = IntVector3()
        if rayHit is None: rayHit = FloatVector3()
        if statMultipliers is None: statMultipliers = StatMultipliers()
        if superWeird is None: superWeird = IntVector3()
        if spawnPosition is None: spawnPosition = LongVector3()
        if unkIntVec3 is None: unkIntVec3 = IntVector3()
        if consumable is None: consumable = Item()
        if equipment is None: equipment = Equipment()
        
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
        self.statMultipliers = statMultipliers
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
        self.equipment = equipment
        self.skills = skills
        self.manaCubes = manaCubes
        self.name = name

    @staticmethod
    def Import(data):     
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
        statMultipliers = StatMultipliers.Import(data)
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
        equipment = Equipment.Import(data)
        skills = struct.unpack('<iiiiiiiiiii', data.read(4*11))
        manaCubes, = struct.unpack('<i', data.read(4))
        name = ''.join([chr(x) for x in data.read(16).rstrip(b'\x00')]) #this method might be slightly more resilient than a decoder
        return Creature(position, orientation, velocity, acceleration, retreat, headRotation, physicsFlags, hostility,
                 unusedByte1, unusedByte2, unusedByte3, creatureType, mode, unusedByte4, unusedByte5, unusedByte6,
                 modeTimer, combo, lastHitTime, appearance, creatureFlags, unusedByte7, unusedByte8, rollTime, stunTime,
                 slowedTime, iceEffectTime, windEffectTime, showPatchTime, classType, specialization, unusedByte9,
                 unusedByte10, chargedMP, unkIntVec1, unkIntVec2, rayHit, HP, MP, blockPower, statMultipliers, unkByte1,
                 unkByte2, unusedByte11, unusedByte12, level, XP, parentOwner, unkLong1, powerBase, unusedByte13,
                 unusedByte14, unusedByte15, unkInt1, superWeird, unkInt2, spawnPosition, unkIntVec3, unkByte3,
                 unusedByte16, unusedByte17, unusedByte18, consumable, equipment, skills, manaCubes, name)

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
        dataList.append(self.statMultipliers.Export())
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
        dataList.append(self.equipment.Export())
        dataList.append(struct.pack('<iiiiiiiiiii', *self.skills))
        dataList.append(struct.pack('<i', self.manaCubes))
        dataList.append(bytes([ord(x)&0xFF for x in self.name]) + b'\x00'*(16-len(self.name)))
        return b''.join(dataList)
    

