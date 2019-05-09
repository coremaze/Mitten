import struct
class LongVector3():
    size = 24
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    @classmethod
    def Import(data):
        x, y, z = struct.unpack("<qqq")
        return LongVector3(x, y, z)
    def Export(self):
        return struct.unpack("<qqq", self.x, self.y, self.z)
