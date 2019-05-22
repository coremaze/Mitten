import struct
import io
from .Packet import Packet
from CubeTypes import Projectile
class ShootPacket(Packet):
    pID = 0x9
    def __init__(self, projectile):
        self.projectile = projectile

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        projectile = Projectile.Import(io.BytesIO(recv(Projectile.size)))
        
        return ShootPacket(projectile)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ShootPacket.pID) )
        packetByteList.append( self.projectile.Export() )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
