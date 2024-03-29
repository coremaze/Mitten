from CubeTypes.FloatVector3 import FloatVector3
import struct

class Sound():
    size = 24
    def __init__(self,
                 position = None,
                 ID = 0,
                 pitch = 0.0,
                 volume = 0.0):

        if position is None: position = FloatVector3()
        
        self.position = position
        self.ID = ID
        self.pitch = pitch
        self.volume = volume
    @staticmethod
    def Import(data):
        position = FloatVector3.Import(data)
        ID, = struct.unpack('<i', data.read(4))
        pitch, = struct.unpack('<f', data.read(4))
        volume, = struct.unpack('<f', data.read(4))
        return Sound(position, ID, pitch, volume)
    def Export(self):
        dataList = []
        dataList.append(self.position.Export())
        dataList.append(struct.pack('<i', self.ID))
        dataList.append(struct.pack('<f', self.pitch))
        dataList.append(struct.pack('<f', self.volume))
        data = b''.join(dataList)
        assert(len(data) == self.size)
        return data
    
