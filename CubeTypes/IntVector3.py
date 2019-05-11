import struct
class IntVector3():
    size = 12
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    @classmethod
    def Import(data):
        x, y, z = struct.unpack("<iii")
        return LongVector3(x, y, z)
    def Export(self):
        return struct.pack("<iii", self.x, self.y, self.z)
