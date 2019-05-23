import struct

class Kill():
    size = 24
    def __init__(self, killer = 0, killed = 0, unknownInt = 0, XP = 0):
        self.killer = killer
        self.killed = killed
        self.unknownInt = unknownInt
        self.XP = XP

    @staticmethod
    def Import(data):
        killer, = struct.unpack('<q', data.read(8))
        killed, = struct.unpack('<q', data.read(8))
        unknownInt, = struct.unpack('<i', data.read(4))
        XP, = struct.unpack('<i', data.read(4))
        return Kill(killer, killed, unknownInt, XP)

    def Export(self):
        dataList = []
        dataList.append( struct.pack('<q', self.killer) )
        dataList.append( struct.pack('<q', self.killed) )
        dataList.append( struct.pack('<i', self.unknownInt) )
        dataList.append( struct.pack('<i', self.XP) )
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
