import struct
import io
from CubeTypes import LongVector3
from CubeTypes import FloatVector3

class Airship():
    size = 120
    def __init__(self, ID, position, velocity, rotation, station, pathRotation, destination, flightState):
        self.id = ID
        self.position       = position
        self.velocity       = velocity
        self.rotation       = rotation
        self.station        = station
        self.pathRotation   = pathRotation
        self.destination    = destination
        self.flightState    = flightState

    @classmethod
    def Import(data):
        ID,          = struct.unpack('<Q', data.read(8))
        data.read(8)
        pos          = LongVector3.Import(data.read(LongVector3.size))
        vel          = FloatVector3.Import(data.read(FloatVector3.size))
        rot,         = struct.unpack('<f', data.read(4))
        station      = LongVector3.Import(data.read(LongVector3.size))
        pathRot,     = struct.unpack('<f', data.read(4))
        data.read(4)
        dest         = LongVector3.Import(data.read(LongVector3.size))
        flightState, = struct.unpack('<I', data.read(4))
        data.read(4)
        return Airship(ID, pos, vel, rot, station, pathRot, dest, flightState)

    def Export(self):
        packet  = struct.pack('<Q', self.id)
        packet += struct.pack('<Q', 0)
        packet += self.position.Export()
        packet += self.velocity.Export()
        packet += struct.pack('<f', self.rotation)
        packet += self.station.Export()
        packet += struct.pack('<f', self.pathRotation)
        packet += struct.pack('<I', 0)
        packet += self.destination.Export()
        packet += struct.pack('<I', self.flightState)
        packet += struct.pack('<I', 0)
        return packet
    
