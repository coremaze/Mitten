import struct
import io
from CubeTypes.Spirit import Spirit

class Item():
    size = 280
    def __init__(self, itemType, subType, modifier, minusModifier, rarity,
                 material, adapted, level, spirits, numSpirits):
        self.itemType = itemType
        self.subType = subType
        self.modifier = modifier
        self.minusModifier = minusModifier
        self.rarity = rarity
        self.material = material
        self.adapted = adapted
        self.level = level
        self.spirits = spirits
        self.numSpirits = numSpirits

    @classmethod
    def Import(self, data):
        itemType, = struct.unpack('<B', data.read(1))
        subType, = struct.unpack('<B', data.read(1))
        data.read(2) #padding
        modifier, = struct.unpack('<I', data.read(4))
        minusModifier, = struct.unpack('<I', data.read(4))
        rarity, = struct.unpack('<B', data.read(1))
        material, = struct.unpack('<B', data.read(1))
        adapted, = struct.unpack('<B', data.read(1))
        data.read(1) #padding
        level, = struct.unpack('<h', data.read(2))
        data.read(2) #padding
        spirits = [Spirit.Import(data) for _ in range(32)]
        numSpirits, = struct.unpack('<I', data.read(4))
        return Item(itemType, subType, modifier, minusModifier, rarity,
                    material, adapted, level, spirits, numSpirits)

    def Export(self):
        dataList = []
        dataList.append(struct.pack('<B', self.itemType))
        dataList.append(struct.pack('<B', self.subType))
        dataList.append(b'\x00\x00') #padding
        dataList.append(struct.pack('<I', self.modifier))
        dataList.append(struct.pack('<B', self.rarity))
        dataList.append(struct.pack('<B', self.material))
        dataList.append(struct.pack('<B', self.adapted))
        dataList.append(b'\x00') #padding
        dataList.append(struct.pack('<h', self.level))
        dataList.append(b'\x00\x00') #padding
        dataList.extend([s.Export() for s in self.spirits])
        dataList.append(struct.pack('<I', self.numSpirits))
        return b''.join(datList)
