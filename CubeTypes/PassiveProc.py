import struct
class PassiveProc():
    size = 40
    def __init__(self, source, target, procType, modifier, duration, unknownInt, poisonSource):
        self.source = source
        self.target = target
        self.procType = procType
        self.modifier = modifier
        self.duration = duration
        self.unknownInt = unknownInt
        self.poisonSource = poisonSource

    @staticmethod
    def Import(data):
        source, = struct.unpack('<q', data.read(8))
        target, = struct.unpack('<q', data.read(8))
        procType, = struct.unpack('<i', data.read(4))
        modifier, = struct.unpack('<f', data.read(4))
        duration, = struct.unpack('<i', data.read(4))
        unknownInt, = struct.unpack('<i', data.read(4))
        poisonSource, = struct.unpack('<q', data.read(8))
        
        return PassiveProc(source, target, procType, modifier, duration, unknownInt, poisonSource)

    def Export(self):
        dataList = []
        dataList.append( struct.pack('<q', self.source) )
        dataList.append( struct.pack('<q', self.target) )
        dataList.append( struct.pack('<i', self.procType) )
        dataList.append( struct.pack('<f', self.modifier) )
        dataList.append( struct.pack('<i', self.duration) )
        dataList.append( struct.pack('<i', self.unknownInt) )
        dataList.append( struct.pack('<q', self.poisonSource) )
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
