import struct
class FloatVector3():
    size = 12
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    @staticmethod
    def Import(data):
        x, y, z = struct.unpack("<fff", data.read(3*4))
        return FloatVector3(x, y, z)
    def Export(self):
        return struct.pack("<fff", self.x, self.y, self.z)
