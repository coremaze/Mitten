import struct
import io
from CubeTypes import LongVector3
from CubeTypes import FloatVector3
from net import recv2
from .Packet import Packet
class HitPacket(Packet):
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
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        attackerID,  = struct.unpack('<Q', recv(8))
        targetID,    = struct.unpack('<Q', recv(8))
        damage,      = struct.unpack('<f', recv(4))
        isCritical,  = struct.unpack('<I', recv(4))
        stunDur,     = struct.unpack('<I', recv(4))
        recv(4) # Padding
        hitPos       = LongVector3.Import(recv(8*3))
        hitDir       = FloatVector3.Import(recv(4*3))
        isYellow,    = struct.unpack('<?', recv(1))
        hitType,     = struct.unpack('<B', recv(1))
        showLight,   = struct.unpack('<?', recv(1))
        recv(1) # Padding

        return HitPacket(attackerID, targetID, damage, isCritical, stunDur, hitPos,
            hitDir, isYellow, hitType, showLight)

    def Export(self, toServer):
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

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
