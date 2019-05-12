import struct
import io
from .Packet import Packet
class ServerFullPacket(Packet):
    pID = 0x12
    def __init__(self):
        pass

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient] 
        return ServerFullPacket()

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ServerFullPacket.pID) )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
