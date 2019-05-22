import struct
import io
from CubeTypes import LongVector3
from CubeTypes import FloatVector3
from CubeTypes import Hit
from .Packet import Packet
class HitPacket(Packet):
    pID = 0x7
    def __init__(self, hit):
        self.hit = hit
        
    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        hit = Hit.Import(io.BytesIO(recv(Hit.size)))

        return HitPacket(hit)

    def Export(self, toServer):
        packet  = struct.pack('<I', HitPacket.pID)
        packet += self.hit.Export()

        return packet

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
