import struct

class Damage():
    size = 24
    def __init__(self, target, attacker, damage, unknownInt):
        self.target = target
        self.attacker = attacker
        self.damage = damage
        self.unknownInt = unknownInt

    @staticmethod
    def Import(data):
        target, = struct.unpack('<q', data.read(8))
        attacker, = struct.unpack('<q', data.read(8))
        damage, = struct.unpack('<f', data.read(4))
        unknownInt, = struct.unpack('<i', data.read(4))
        return Damage(target, attacker, damage, unknownInt)

    def Export(self):
        dataList = []
        dataList.append( struct.pack('<q', self.target) )
        dataList.append( struct.pack('<q', self.attacker) )
        dataList.append( struct.pack('<f', self.damage) )
        dataList.append( struct.pack('<i', self.unknownInt) )
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
