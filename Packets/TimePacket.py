import struct
import io
from .Packet import Packet
class TimePacket(Packet):
    pID = 0x5
    def __init__(self, day=0, time=0):
        self.day  = day
        self.time = time
    
    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        day,  = struct.unpack('<I', recv(4))
        time, = struct.unpack('<I', recv(4))
        return TimePacket(day, time)

    def Export(self, toServer):
        packet  = struct.pack('<I', TimePacket.pID)
        packet += struct.pack('<I', self.day)
        packet += struct.pack('<I', self.time)
        return packet

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
        
