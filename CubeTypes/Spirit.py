import struct
import io

class Spirit():
    size = 8
    def __init__(x, y, z, material, level):
        self.x = x
        self.y = y
        self.z = z
        self.material = material
        self.level = level

    @classmethod
    def Import(data):
        x, = struct.unpack('<B', data.read(1))
        y, = struct.unpack('<B', data.read(1))
        z, = struct.unpack('<B', data.read(1))
        material, = struct.unpack('<B', data.read(1))
        level, = struct.unpack('<h', data.read(1))
        data.read(2) #padding
        return Spirit(x, y, z, material, level)

    def Export(self):
        dataList = []
        dataList.append(struct.pack('<B', self.x))
        dataList.append(struct.pack('<B', self.y))
        dataList.append(struct.pack('<B', self.z))
        dataList.append(struct.pack('<B', self.material))
        dataList.append(struct.pack('<h', self.level))
        dataList.append(b'\x00\x00') #padding
        return b''.join(dataList)
