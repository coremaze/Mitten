from CubeTypes.LongVector3 import LongVector3
from CubeTypes.FloatVector3 import FloatVector3
import struct

class Particle():
    size = 72
    def __init__(self, position, acceleration, red, green, blue, alpha,
                 scale, count, _type, spreading, unkInt):
        self.position = position
        self.acceleration = acceleration
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        self.scale = scale
        self.count = count
        self.type = _type
        self.spreading = spreading
        self.unkInt = unkInt
    @staticmethod
    def Import(data):
        position = LongVector3.Import(data)
        acceleration = FloatVector3.Import(data)
        red, = struct.unpack('<f', data.read(4))
        green, = struct.unpack('<f', data.read(4))
        blue, = struct.unpack('<f', data.read(4))
        alpha, = struct.unpack('<f', data.read(4))
        scale, = struct.unpack('<f', data.read(4))
        count, = struct.unpack('<i', data.read(4))
        _type, = struct.unpack('<i', data.read(4))
        spreading, = struct.unpack('<f', data.read(4))
        unkInt, = struct.unpack('<i', data.read(4))
        return Particle(position, acceleration, red, green, blue, alpha,
                 scale, count, _type, spreading, unkInt)
    def Export(self):
        dataList = []
        dataList.append(self.position.Export())
        dataList.append(self.acceleration.Export())
        dataList.append(struct.pack('<f', self.red))
        dataList.append(struct.pack('<f', self.green))
        dataList.append(struct.pack('<f', self.blue))
        dataList.append(struct.pack('<f', self.alpha))
        dataList.append(struct.pack('<f', self.scale))
        dataList.append(struct.pack('<i', self.count))
        dataList.append(struct.pack('<i', self.type))
        dataList.append(struct.pack('<f', self.spreading))
        dataList.append(struct.pack('<i', self.unkInt))
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
    
