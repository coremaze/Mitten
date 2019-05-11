import struct
import io
from net import recv2
from .Packet import Packet
class TimePacket(Packet):
    pID = 0x5
    def __init__(self, day, time):
        self.day  = day
        self.time = time
    
    @staticmethod
    def Recv(sock):
        day,  = struct.unpack('<I', recv2(sock, 4))
        time, = struct.unpack('<I', recv2(sock, 4))
        return TimePacket(day,time)

    def Export(self):
        packet  = struct.pack('<I', pID)
        packet += struct.pack('<I', self.day)
        packet += struct.pack('<I', self.time)
        return packet

    def Send(self, sock):
        return sock.send(self.Export())
        
