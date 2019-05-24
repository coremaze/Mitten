import struct
import io
from CubeTypes.Spirit import Spirit

class Item():
    size = 280
    def __init__(self,
                 itemType = 0,
                 subType = 0,
                 unkShort1 = 0,
                 modifier = 0,
                 minusModifier = 0,
                 rarity = 0,
                 material = 0,
                 adapted = 0,
                 unkByte = 0,
                 level = 0,
                 unkShort2 = 0,
                 spirits = None,
                 numSpirits = 0):

        if spirits is None: spirits = [Spirit() for _ in range(32)]
        
        self.itemType = itemType
        self.subType = subType
        self.unkShort1 = unkShort1
        self.modifier = modifier
        self.minusModifier = minusModifier
        self.rarity = rarity
        self.material = material
        self.adapted = adapted
        self.unkByte = unkByte
        self.level = level
        self.unkShort2 = unkShort2
        if len(spirits) != 32:
            raise ValueError('An Item must have 32 Spirits.')
        self.spirits = spirits
        self.numSpirits = numSpirits

    @staticmethod
    def Import(data):
        itemType, = struct.unpack('<B', data.read(1))
        subType, = struct.unpack('<B', data.read(1))
        unkShort1, = struct.unpack('<h', data.read(2))
        modifier, = struct.unpack('<I', data.read(4))
        minusModifier, = struct.unpack('<I', data.read(4))
        rarity, = struct.unpack('<B', data.read(1))
        material, = struct.unpack('<B', data.read(1))
        adapted, = struct.unpack('<B', data.read(1))
        unkByte, = struct.unpack('<B', data.read(1))
        level, = struct.unpack('<h', data.read(2))
        unkShort2, = struct.unpack('<h', data.read(2))
        spirits = [Spirit.Import(data) for _ in range(32)]
        numSpirits, = struct.unpack('<I', data.read(4))
        return Item(itemType, subType, unkShort1, modifier, minusModifier, rarity,
                    material, adapted, unkByte, level, unkShort2, spirits, numSpirits)

    def Export(self):
        dataList = []
        dataList.append(struct.pack('<B', self.itemType))
        dataList.append(struct.pack('<B', self.subType))
        dataList.append(struct.pack('<h', self.unkShort1))
        dataList.append(struct.pack('<I', self.modifier))
        dataList.append(struct.pack('<I', self.minusModifier))
        dataList.append(struct.pack('<B', self.rarity))
        dataList.append(struct.pack('<B', self.material))
        dataList.append(struct.pack('<B', self.adapted))
        dataList.append(struct.pack('<B', self.unkByte))
        dataList.append(struct.pack('<h', self.level))
        dataList.append(struct.pack('<h', self.unkShort2))
        dataList.extend([s.Export() for s in self.spirits])
        dataList.append(struct.pack('<I', self.numSpirits))
        return b''.join(dataList)
