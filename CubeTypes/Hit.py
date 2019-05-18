import struct
import io
from CubeTypes import LongVector3
from CubeTypes import FloatVector3

class Hit():
    size = 72
    def __init__(self, attackerID, targetID, dmg, isCrit, stunDur, unkInt,
            hitPos, hitDir, isYellow, hitType, showLight, unkByte ):
        self.attackerID = attackerID
        self.targetID   = targetID
        self.dmg        = dmg
        self.isCrit     = isCrit
        self.stunDur    = stunDur
        self.unkInt     = unkInt
        self.hitPos     = hitPos
        self.hitDir     = hitDir
        self.isYellow   = isYellow
        self.hitType    = hitType
        self.showLight  = showLight
        self.unkByte    = unkByte


    @staticmethod
    def Import(data):
        attackerID,  = struct.unpack('<Q', data.read(8))
        targetID,    = struct.unpack('<Q', data.read(8))
        damage,      = struct.unpack('<f', data.read(4))
        isCritical,  = struct.unpack('<I', data.read(4))
        stunDur,     = struct.unpack('<I', data.read(4))
        unkInt,      = struct.unpack('<I', data.read(4))
        hitPos       = LongVector3.Import(data)
        hitDir       = FloatVector3.Import(data)
        isYellow,    = struct.unpack('<?', data.read(1))
        hitType,     = struct.unpack('<B', data.read(1))
        showLight,   = struct.unpack('<?', data.read(1))
        unkByte,     = struct.unpack('<B', data.read(1))

        return Hit(attackerID, targetID, damage, isCritical, stunDur, unkInt, hitPos,
            hitDir, isYellow, hitType, showLight, unkByte)

    def Export(self):
        dataList = []
        dataList.append(struct.pack('<Q', self.attackerID))
        dataList.append(struct.pack('<Q', self.targetID))
        dataList.append(struct.pack('<f', self.dmg))
        dataList.append(struct.pack('<I', self.isCrit))
        dataList.append(struct.pack('<I', self.stunDur))
        dataList.append(struct.pack('<I', self.unkInt)) # Padding
        dataList.append(self.hitPos.Export())
        dataList.append(self.hitDir.Export())
        dataList.append(struct.pack('<?', self.isYellow))
        dataList.append(struct.pack('<B', self.hitType))
        dataList.append(struct.pack('<?', self.showLight))
        dataList.append(struct.pack('<B', self.unkByte)) # Padding
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data

