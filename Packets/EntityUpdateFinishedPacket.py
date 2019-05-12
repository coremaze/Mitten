import struct
import io
from .Packet import Packet
class EntityUpdateFinishedPacket(Packet):
    pID = 0x2
    def __init__(self):
        pass

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient] 
        return EntityUpdateFinishedPacket()

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', EntityUpdateFinishedPacket.pID) )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
