import struct
from CubeTypes.Vector3 import Vector3
class FloatVector3(Vector3):
    size = 12
    @staticmethod
    def Import(data):
        x, y, z = struct.unpack("<fff", data.read(3*4))
        return FloatVector3(x, y, z)
    def Export(self):
        return struct.pack("<fff", self.x, self.y, self.z)
