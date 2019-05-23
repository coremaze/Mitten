import struct
import io
from .Packet import Packet
from CubeTypes import Creature
class JoinPacket(Packet):
    pID = 0x10
    def __init__(self, unknown = 0, creatureID = 0, creature = Creature()):
        self.unknown = unknown
        self.creatureID = creatureID
        self.creature = creature

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        unknown, = struct.unpack('<I', recv(4))
        creatureID, = struct.unpack('<q', recv(8))
        creature = Creature.Import(io.BytesIO(recv(Creature.size)))
            
        return JoinPacket(unknown, creatureID, creature)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', JoinPacket.pID) )
        packetByteList.append( struct.pack('<I', self.unknown) )
        packetByteList.append( struct.pack('<q', self.creatureID) )
        packetByteList.append( self.creature.Export() )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
