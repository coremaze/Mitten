import struct
import io
from .Packet import Packet
class MapSeedPacket(Packet):
    pID = 0xF
    def __init__(self, seed):
        self.seed = seed

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        seed, = struct.unpack('<I', recv(4))
            
        return MapSeedPacket(seed)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', MapSeedPacket.pID) )
        packetByteList.append( struct.pack('<I', self.seed) )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
