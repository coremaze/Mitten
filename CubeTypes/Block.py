from CubeTypes.IntVector3 import IntVector3
import struct

class Block():
    size = 20
    def __init__(self, position, red, green, blue, _type, unkInt):
        self.position = position
        self.red = red
        self.green = green
        self.blue = blue
        self.type = _type
        self.unkInt = unkInt
    @staticmethod
    def Import(data):
        position = IntVector3.Import(data)
        red, = struct.unpack('<B', data.read(1))
        green, = struct.unpack('<B', data.read(1))
        blue, = struct.unpack('<B', data.read(1))
        _type, = struct.unpack('<B', data.read(1))
        unkInt, = struct.unpack('<i', data.read(4))
        return Block(position, red, green, blue, _type, unkInt)
    def Export(self):
        dataList = []
        dataList.append(self.position.Export())
        dataList.append(struct.pack('<B', self.red))
        dataList.append(struct.pack('<B', self.green))
        dataList.append(struct.pack('<B', self.blue))
        dataList.append(struct.pack('<B', self.type))
        dataList.append(struct.pack('<i', self.unkInt))
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
    
