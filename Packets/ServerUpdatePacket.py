import struct
import io
from .Packet import Packet
import zlib
class ServerUpdatePacket(Packet):
    pID = 0x4
    def __init__(self, zlibData):
        self.zlibData = zlibData #let's actually parse this eventually

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        size, = struct.unpack('<I', recv(4))
        zlibData = recv(size)
            
        return ServerUpdatePacket(zlibData)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ServerUpdatePacket.pID) )
        packetByteList.append( struct.pack('<I', len(self.zlibData)) )
        packetByteList.append( self.zlibData )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
