from CubeTypes.LongVector3 import LongVector3
from CubeTypes.FloatVector3 import FloatVector3
import struct

class StaticEntity():
    size = 88
    def __init__(self, zoneX, zoneY, ID, unknownInt1, _type, unknownInt2,
                 position, rotation, size, closed, time, unknownInt3,
                 unknownInt4, user):
        self.zoneX = zoneX
        self.zoneY = zoneY
        self.ID = ID
        self.unknownInt1 = unknownInt1
        self.type = _type
        self.unknownInt2 = unknownInt2
        self.position = position
        self.rotation = rotation
        self.size = size
        self.closed = closed
        self.time = time
        self.unknownInt3 = unknownInt3
        self.unknownInt4 = unknownInt4
        self.user = user
    @staticmethod
    def Import(data):
        zoneX, = struct.unpack('<i', data.read(4))
        zoneY, = struct.unpack('<i', data.read(4))
        unknownInt1, = struct.unpack('<i', data.read(4))
        _type, = struct.unpack('<i', data.read(4))
        unknownInt2, = struct.unpack('<i', data.read(4))
        position = LongVector3.Import(data)
        rotation, = struct.unpack('<f', data.read(4))
        size = FloatVector3.Import(data)
        closed, = struct.unpack('<i', data.read(4))
        time, = struct.unpack('<i', data.read(4))
        unknownInt3, = struct.unpack('<i', data.read(4))
        unknownInt4, = struct.unpack('<i', data.read(4))
        user, = struct.unpack('<q', data.read(8))
        return StaticEntity(zoneX, zoneY, ID, unknownInt1, _type, unknownInt2,
                 position, rotation, size, closed, time, unknownInt3,
                 unknownInt4, user)
    def Export(self):
        dataList = []
        dataList.append(struct.pack('<i', self.zoneX))
        dataList.append(struct.pack('<i', self.zoneY))
        dataList.append(struct.pack('<i', self.unknownInt1))
        dataList.append(struct.pack('<i', self.type))
        dataList.append(struct.pack('<i', self.unknownInt2))
        dataList.append(self.position.Export())
        dataList.append(struct.pack('<f', self.rotation))
        dataList.append(self.size.Export())
        dataList.append(struct.pack('<i', self.closed))
        dataList.append(struct.pack('<i', self.time))
        dataList.append(struct.pack('<i', self.unknownInt3))
        dataList.append(struct.pack('<i', self.unknownInt4))
        dataList.append(struct.pack('<q', self.user))
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
    
