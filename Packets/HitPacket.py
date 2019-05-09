import struct
import io
import CubeTypes.LongVector3
import CubeTypes.FloatVector3
class HitPacket():
    pID = 0x7
    def __init__(self, attackerID, targetID, dmg, isCrit, stunDur, hitPos,
        hitDir, isYellow, hitType, showLight ):
        self.attackerID = attackerID
        self.targetID   = targetID
        self.dmg        = dmg
        self.isCrit     = isCrit
        self.stunDur    = stunDur
        self.hitPos     = hitPos
        self.hitDir     = hitDir
        self.isYellow   = isYellow
        self.hitType    = hitType
        self.showLight  = showLight

    @staticmethod
    def Import(data):
        dID = struct.unpack('<I', data.read(4))
        if (pID is not dID) :
            raise ValueError(f'Received packet ID of {dID} when {pID} was expected.')

        attackerID  = struct.unpack('<Q', data.read(8))
        targetID    = struct.unpack('<Q', data.read(8))
        damage      = struct.unpack('<f', data.read(4))
        isCritical  = struct.unpack('<I', data.read(4))
        stunDur     = struct.unpack('<I', data.read(4))
        data.read(4) # Padding
        hitPos      = LongVector3.Import(data.read(8*3))
        hitDir      = FloatVector3.Import(data.read(8*3))
        isYellow    = struct.unpack('<?', data.read(1))
        hitType     = struct.unpack('<B', data.read(1))
        showLight   = struct.unpack('<?', data.read(1))
        data.read(1) # Padding

        return HitPacket(attackerID, targetID, damage, isCritical, stunDur, hitPos,
            hitDir, isYellow, hitType, showLight)

    def Export(self):
        packet  = struct.pack('<I', pID)
        packet += struct.pack('<Q', self.attackerID)
        packet += struct.pack('<Q', self.targetID)
        packet += struct.pack('<f', self.dmg)
        packet += struct.pack('<I', self.isCrit)
        packet += struct.pack('<I', self.stunDur)
        packet += struct.pack('<I', 0) # Padding
        packet += self.hitPos.Export()
        packet += self.hitDir.Export()
        packet += struct.pack('<?', self.isYellow)
        packet += struct.pack('<B', self.hitType)
        packet += struct.pack('<?', self.showLight)
        packet += struct.pack('<B',0) # Padding

        return packet

    def Send(self, sock):
        return sock.send(self.Export())
