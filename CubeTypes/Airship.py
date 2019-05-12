import struct
import io
from CubeTypes.LongVector3 import LongVector3
from CubeTypes.FloatVector3 import FloatVector3

class Airship():
    size = 120
    def __init__(self, ID, unkInt1, unkInt2, position, velocity, rotation, station, pathRotation, unkInt3,
                 destination, flightState, unkInt4):
        self.ID = ID
        self.unkInt1 = unkInt1
        self.unkInt2 = unkInt2
        self.position = position
        self.velocity = velocity
        self.rotation = rotation
        self.station = station
        self.pathRotation = pathRotation
        self.unkInt3 = unkInt3
        self.destination = destination
        self.flightState = flightState
        self.unkInt4 = unkInt4
        

    @classmethod
    def Import(self, data):
        ID, = struct.unpack('<q', data.read(8))
        unkInt1, = struct.unpack('<I', data.read(4))
        unkInt2, = struct.unpack('<I', data.read(4))
        position = LongVector3.Import(data)
        velocity = FloatVector3.Import(data)
        rotation, = struct.unpack('<f', data.read(4))
        station = LongVector3.Import(data)
        pathRotation, = struct.unpack('<f', data.read(4))
        unkInt3, = struct.unpack('<I', data.read(4))
        destination = LongVector3.Import(data)
        flightState, = struct.unpack('<I', data.read(4))
        unkInt4, = struct.unpack('<I', data.read(4))
        
        return Airship(ID, unkInt1, unkInt2, position, velocity, rotation, station, pathRotation, unkInt3,
                 destination, flightState, unkInt4)

    def Export(self):
        dataList = []
        dataList.append(struct.pack('<q', self.ID))
        dataList.append(struct.pack('<I', self.unkInt1))
        dataList.append(struct.pack('<I', self.unkInt2))
        dataList.append(self.position.Export())
        dataList.append(self.velocity.Export())
        dataList.append(struct.pack('<f', self.rotation))
        dataList.append(self.station.Export())
        dataList.append(struct.pack('<f', self.pathRotation))
        dataList.append(struct.pack('<I', self.unkInt3))
        dataList.append(self.destination.Export())
        dataList.append(struct.pack('<I', self.flightState))
        dataList.append(struct.pack('<I', self.unkInt4))
        return b''.join(dataList)
    
