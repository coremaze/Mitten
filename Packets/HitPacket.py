import struct
import io
from CubeTypes import LongVector3
from CubeTypes import FloatVector3
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
    def Recv(sock):
        attackerID,  = struct.unpack('<Q', recv2(sock, 8))
        targetID,    = struct.unpack('<Q', recv2(sock, 8))
        damage,      = struct.unpack('<f', recv2(sock, 4))
        isCritical,  = struct.unpack('<I', recv2(sock, 4))
        stunDur,     = struct.unpack('<I', recv2(sock, 4))
        recv2(sock, 4) # Padding
        hitPos       = LongVector3.Import(recv2(sock, 8*3))
        hitDir       = FloatVector3.Import(recv2(sock, 4*3))
        isYellow,    = struct.unpack('<?', recv2(sock, 1))
        hitType,     = struct.unpack('<B', recv2(sock, 1))
        showLight,   = struct.unpack('<?', recv2(sock, 1))
        recv2(sock, 1) # Padding

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
