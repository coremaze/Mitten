import struct
from CubeTypes import Item
from CubeTypes import LongVector3

class Drop():
    size = 328
    def __init__(self,
                 item = None,
                 position = None,
                 rotation = 0.0,
                 scale = 0.0,
                 unknownInt1 = 0,
                 time = 0,
                 unknownInt2 = 0,
                 unknownInt3 = 0):

        if item is None: item = Item()
        if position is None: position = LongVector3()

        self.item = item
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.unknownInt1 = unknownInt1
        self.time = time
        self.unknownInt2 = unknownInt2
        self.unknownInt3 = unknownInt3
    @staticmethod
    def Import(data):
        item = Item.Import(data)
        position = LongVector3.Import(data)
        rotation, = struct.unpack('<f', data.read(4))
        scale, = struct.unpack('<f', data.read(4))
        unknownInt1, = struct.unpack('<i', data.read(4))
        time, = struct.unpack('<i', data.read(4))
        unknownInt2, = struct.unpack('<i', data.read(4))
        unknownInt3, = struct.unpack('<i', data.read(4))
        return Drop(item, position, rotation, scale, unknownInt1,
                 time, unknownInt2, unknownInt3)
    def Export(self):
        dataList = []
        dataList.append(self.item.Export())
        dataList.append(self.position.Export())
        dataList.append(struct.pack('<f', self.rotation))
        dataList.append(struct.pack('<f', self.scale))
        dataList.append(struct.pack('<i', self.unknownInt1))
        dataList.append(struct.pack('<i', self.time))
        dataList.append(struct.pack('<i', self.unknownInt2))
        dataList.append(struct.pack('<i', self.unknownInt3))
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
    
