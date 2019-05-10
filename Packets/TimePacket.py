import struct
import io
class TimePacket():
    pID = 0x5
    def __init__(self, day, time):
        self.day  = day
        self.time = time
    
    @staticmethod
    def Import(data):
        dID, = struct.unpack('<I', data.read(4))
        if (TimePacket.pID is not dID) :
            raise ValueError(f'Received packet ID of {dID} when {TimePacket.pID} was expected.')

        day,  = struct.unpack('<I', data.read(4))
        time, = struct.unpack('<I', data.read(4))
        return TimePacket(day,time)

    def Export(self):
        packet  = struct.pack('<I', pID)
        packet += struct.pack('<I', self.day)
        packet += struct.pack('<I', self.time)
        return packet

    def Send(self, sock):
        return sock.send(self.Export())
