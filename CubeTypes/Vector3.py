import math
class Vector3():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def Dist(self, other):
        x1, y1, z1 = self.x, self.y, self.z
        x2, y2, z2 = other.x, other.y, other.z
        return math.sqrt( (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
    @staticmethod
    def Import(data):
        raise NotImplemented('Method not implemented.')
    def Export(self):
        raise NotImplemented('Method not implemented.')
