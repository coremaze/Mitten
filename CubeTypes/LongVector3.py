import struct
from CubeTypes.Vector3 import Vector3
class LongVector3(Vector3):
    size = 24
    @staticmethod
    def Import(data):
        x, y, z = struct.unpack("<qqq", data.read(3*8))
        return LongVector3(x, y, z)
    def Export(self):
        return struct.pack("<qqq", self.x, self.y, self.z)
