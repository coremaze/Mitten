import struct
import io
from .Packet import Packet
from CubeTypes import CreatureDelta
class EntityUpdatePacket(Packet):
    pID = 0x0
    def __init__(self, creatureDelta):
        self.creatureDelta = creatureDelta

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        size, = struct.unpack('<I', recv(4))
        creatureDelta = CreatureDelta.Import(recv(size))
        return EntityUpdatePacket(creatureDelta)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', EntityUpdatePacket.pID) )
        zlibData = self.creatureDelta.Export()
        packetByteList.append( struct.pack('<I', len(zlibData)) )
        packetByteList.append( zlibData )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
