import struct
import io
from .Packet import Packet
class VersionPacket(Packet):
    pID = 0x11
    def __init__(self, versionNumber):
        self.versionNumber = versionNumber

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        versionNumber, = struct.unpack('<I', recv(4))
        return VersionPacket(versionNumber)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', VersionPacket.pID) )
        packetByteList.append( struct.pack('<I', self.versionNumber) )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
