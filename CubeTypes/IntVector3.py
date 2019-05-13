import struct
from CubeTypes.Vector3 import Vector3
class IntVector3(Vector3):
    size = 12
    @staticmethod
    def Import(data):
        x, y, z = struct.unpack("<iii", data.read(3*4))
        return IntVector3(x, y, z)
    def Export(self):
        return struct.pack("<iii", self.x, self.y, self.z)
