import struct
from CubeTypes import Item

class Pickup():
    size = 288
    def __init__(self, guid, item):
        self.guid = guid
        self.item = item
    @staticmethod
    def Import(data):
        guid, = struct.unpack('<q', data.read(8))
        item = Item.Import(data)
        return Pickup(guid, item)
    def Export(self):
        dataList = []
        dataList.append(struct.pack('<q', self.guid))
        dataList.append(self.item.Export())
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
    
