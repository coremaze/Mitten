import struct
import io

class Spirit():
    size = 8
    def __init__(self, x, y, z, material, level, unkShort):
        self.x = x
        self.y = y
        self.z = z
        self.material = material
        self.level = level
        self.unkShort = unkShort

    @staticmethod
    def Import(data):
        x, = struct.unpack('<B', data.read(1))
        y, = struct.unpack('<B', data.read(1))
        z, = struct.unpack('<B', data.read(1))
        material, = struct.unpack('<B', data.read(1))
        level, = struct.unpack('<h', data.read(2))
        unkShort, = struct.unpack('<h', data.read(2))
        return Spirit(x, y, z, material, level, unkShort)

    def Export(self):
        dataList = []
        dataList.append(struct.pack('<B', self.x))
        dataList.append(struct.pack('<B', self.y))
        dataList.append(struct.pack('<B', self.z))
        dataList.append(struct.pack('<B', self.material))
        dataList.append(struct.pack('<h', self.level))
        dataList.append(struct.pack('<h', self.unkShort))
        return b''.join(dataList)
