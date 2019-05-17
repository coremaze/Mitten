import struct
class Mission():
    size = 56
    def __init__(self, regionX, regionY, unknownInt1, unknownInt2, unknownInt3,
                 missionID, _type, monsterID, level, unknownByte, state, unknownShort,
                 currentHP, maxHP, zoneX, zoneY):
        self.regionX = regionX
        self.regionY = regionY
        self.unknownInt1 = unknownInt1
        self.unknownInt2 = unknownInt2
        self.unknownInt3 = unknownInt3
        self.missionID = missionID
        self.type = _type
        self.monsterID = monsterID
        self.level = level
        self.unknownByte = unknownByte
        self.state = state
        self.unknownShort = unknownShort
        self.currentHP = currentHP
        self.maxHP = maxHP
        self.zoneX = zoneX
        self.zoneY = zoneY
    @staticmethod
    def Import(data):
        regionX, = struct.unpack('<i', data.read(4))
        regionY, = struct.unpack('<i', data.read(4))
        unknownInt1, = struct.unpack('<i', data.read(4))
        unknownInt2, = struct.unpack('<i', data.read(4))
        unknownInt3, = struct.unpack('<i', data.read(4))
        missionID, = struct.unpack('<i', data.read(4))
        _type, = struct.unpack('<i', data.read(4))
        monsterID, = struct.unpack('<i', data.read(4))
        level, = struct.unpack('<i', data.read(4))
        unknownByte, = struct.unpack('<B', data.read(1))
        state, = struct.unpack('<B', data.read(1))
        unknownShort, = struct.unpack('<H', data.read(2))
        currentHP, = struct.unpack('<f', data.read(4))
        maxHP, = struct.unpack('<f', data.read(4))
        zoneX, = struct.unpack('<i', data.read(4))
        zoneY, = struct.unpack('<i', data.read(4))
        return Mission(regionX, regionY, unknownInt1, unknownInt2, unknownInt3,
                 missionID, _type, monsterID, level, unknownByte, state, unknownShort,
                 currentHP, maxHP, zoneX, zoneY)
    def Export(self):
        dataList = []
        dataList.append(struct.pack('<i', self.regionX))
        dataList.append(struct.pack('<i', self.regionY))
        dataList.append(struct.pack('<i', self.unknownInt1))
        dataList.append(struct.pack('<i', self.unknownInt2))
        dataList.append(struct.pack('<i', self.unknownInt3))
        dataList.append(struct.pack('<i', self.missionID))
        dataList.append(struct.pack('<i', self.type))
        dataList.append(struct.pack('<i', self.monsterID))
        dataList.append(struct.pack('<i', self.level))
        dataList.append(struct.pack('<B', self.unknownByte))
        dataList.append(struct.pack('<B', self.state))
        dataList.append(struct.pack('<H', self.unknownShort))
        dataList.append(struct.pack('<f', self.currentHP))
        dataList.append(struct.pack('<f', self.maxHP))
        dataList.append(struct.pack('<i', self.zoneX))
        dataList.append(struct.pack('<i', self.zoneY))
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
    
