import struct
class LongVector3():
    size = 24
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    @staticmethod
    def Import(data):
        x, y, z = struct.unpack("<qqq", data.read(3*8))
        return LongVector3(x, y, z)
    def Export(self):
        return struct.pack("<qqq", self.x, self.y, self.z)
