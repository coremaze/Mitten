import struct
import io
from .Packet import Packet
from CubeTypes import PassiveProc
class PassiveProcPacket(Packet):
    pID = 0x8
    def __init__(self, passiveProc):
        self.passiveProc = passiveProc

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]

        passiveProc = PassiveProc.Import(io.BytesIO(recv(PassiveProc.size)))
        
        return PassiveProcPacket(passiveProc)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', PassiveProcPacket.pID) )
        packetByteList.append( self.passiveProc.Export() )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
