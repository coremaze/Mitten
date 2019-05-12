import struct
import io
from .Packet import Packet
class PassiveProcPacket(Packet):
    pID = 0x8
    def __init__(self, source, target, procType, modifier, duration, unknownInt, poisonSource):
        self.source = source
        self.target = target
        self.procType = procType
        self.modifier = modifier
        self.duration = duration
        self.unknownInt = unknownInt
        self.poisonSource = poisonSource

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]

        source, = struct.unpack('<q', recv(8))
        target, = struct.unpack('<q', recv(8))
        procType, = struct.unpack('<i', recv(4))
        modifier, = struct.unpack('<f', recv(4))
        duration, = struct.unpack('<i', recv(4))
        unknownInt, = struct.unpack('<i', recv(4))
        poisonSource, = struct.unpack('<q', recv(8))
        
        return PassiveProcPacket(source, target, procType, modifier, duration, unknownInt, poisonSource)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', PassiveProcPacket.pID) )
        packetByteList.append( struct.pack('<q', self.source) )
        packetByteList.append( struct.pack('<q', self.target) )
        packetByteList.append( struct.pack('<i', self.procType) )
        packetByteList.append( struct.pack('<f', self.modifier) )
        packetByteList.append( struct.pack('<i', self.duration) )
        packetByteList.append( struct.pack('<i', self.unknownInt) )
        packetByteList.append( struct.pack('<q', self.poisonSource) )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
