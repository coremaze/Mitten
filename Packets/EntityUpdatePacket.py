import struct
import io
from .Packet import Packet
import zlib
class EntityUpdatePacket(Packet):
    pID = 0x0
    def __init__(self, zlibData):
        self.zlibData = zlibData #let's actually parse this eventually

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        size, = struct.unpack('<I', recv(4))
        zlibData = recv(size)
            
        return EntityUpdatePacket(zlibData)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', EntityUpdatePacket.pID) )
        packetByteList.append( struct.pack('<I', len(self.zlibData)) )
        packetByteList.append( self.zlibData )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
