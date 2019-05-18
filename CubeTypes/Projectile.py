from CubeTypes.LongVector3 import LongVector3
from CubeTypes.FloatVector3 import FloatVector3
import struct

class Projectile():
    def __init__(self, creatureID, zoneX, zoneY, unknownInt1, unknownInt2,
                 position, unknownInt3, unknownInt4, unknownInt5, velocity,
                 legacyDamage, unknownFloat1, size, mana, particles, skill,
                 projectile, unknownInt6, unknownInt7, unknownInt8):
        self.creatureID = creatureID
        self.zoneX = zoneX
        self.zoneY = zoneY
        self.unknownInt1 = unknownInt1
        self.unknownInt2 = unknownInt2
        self.position = position
        self.unknownInt3 = unknownInt3
        self.unknownInt4 = unknownInt4
        self.unknownInt5 = unknownInt5
        self.velocity = velocity
        self.legacyDamage = legacyDamage
        self.unknownFloat1 = unknownFloat1
        self.size = size
        self.mana = mana
        self.particles = particles
        self.skill = skill
        self.projectile = projectile
        self.unknownInt6 = unknownInt6
        self.unknownInt7 = unknownInt7
        self.unknownInt8 = unknownInt8

    @staticmethod
    def Import(data):
        creatureID, = struct.unpack('<q', data.read(8)) 
        zoneX, = struct.unpack('<i', data.read(4))
        zoneY, = struct.unpack('<i', data.read(4))
        unknownInt1, = struct.unpack('<i', data.read(4))
        unknownInt2, = struct.unpack('<i', data.read(4))
        position = LongVector3.Import(data)
        unknownInt3, = struct.unpack('<i', data.read(4))
        unknownInt4, = struct.unpack('<i', data.read(4))
        unknownInt5, = struct.unpack('<i', data.read(4))
        velocity = FloatVector3.Import(data)
        legacyDamage, = struct.unpack('<f', data.read(4))
        unknownFloat1, = struct.unpack('<f', data.read(4))
        size, = struct.unpack('<f', data.read(4))
        mana, = struct.unpack('<f', data.read(4))
        particles, = struct.unpack('<i', data.read(4))
        skill, = struct.unpack('<i', data.read(4))
        projectile, = struct.unpack('<i', data.read(4))
        unknownInt6, = struct.unpack('<i', data.read(4))
        unknownInt7, = struct.unpack('<i', data.read(4))
        unknownInt8, = struct.unpack('<i', data.read(4))
        
        return Projectile(creatureID, zoneX, zoneY, unknownInt1, unknownInt2,
                 position, unknownInt3, unknownInt4, unknownInt5, velocity,
                 legacyDamage, unknownFloat1, size, mana, particles, skill,
                 projectile, unknownInt6, unknownInt7, unknownInt8)

    def Export(self):
        packetByteList = []
        packetByteList.append( struct.pack('<q', self.creatureID) )
        packetByteList.append( struct.pack('<i', self.zoneX) )
        packetByteList.append( struct.pack('<i', self.zoneY) )
        packetByteList.append( struct.pack('<i', self.unknownInt1) )
        packetByteList.append( struct.pack('<i', self.unknownInt2) )
        packetByteList.append( self.position.Export() )
        packetByteList.append( struct.pack('<i', self.unknownInt3) )
        packetByteList.append( struct.pack('<i', self.unknownInt4) )
        packetByteList.append( struct.pack('<i', self.unknownInt5) )
        packetByteList.append( self.velocity.Export() )
        packetByteList.append( struct.pack('<f', self.legacyDamage) )
        packetByteList.append( struct.pack('<f', self.unknownFloat1) )
        packetByteList.append( struct.pack('<f', self.size) )
        packetByteList.append( struct.pack('<f', self.mana) )
        packetByteList.append( struct.pack('<i', self.particles) )
        packetByteList.append( struct.pack('<i', self.skill) )
        packetByteList.append( struct.pack('<i', self.projectile) )
        packetByteList.append( struct.pack('<i', self.unknownInt6) )
        packetByteList.append( struct.pack('<i', self.unknownInt7) )
        packetByteList.append( struct.pack('<i', self.unknownInt8) )
        return b''.join(packetByteList)
