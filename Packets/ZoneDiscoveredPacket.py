import struct
import io
from .Packet import Packet
class ZoneDiscoveredPacket(Packet):
    pID = 0xB
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]

        x,  = struct.unpack('<i', recv(4))
        y, = struct.unpack('<i', recv(4))
        return ZoneDiscoveredPacket(x, y)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ZoneDiscoveredPacket.pID) )
        packetByteList.append( struct.pack('<i', self.x) )
        packetByteList.append( struct.pack('<i', self.y) )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
