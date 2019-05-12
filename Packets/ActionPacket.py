import struct
import io
from .Packet import Packet
from CubeTypes.Item import Item
class ActionPacket(Packet):
    pID = 0x6
    def __init__(self, item, zoneX, zoneY, index, unknownInt, interactionType, unkShort):
        self.item = item
        self.zoneX = zoneX
        self.zoneY = zoneY
        self.index = index
        self.unknownInt = unknownInt
        self.interactionType = interactionType
        self.unkShort = unkShort

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]

        item = Item.Import(io.BytesIO(recv(Item.size)))
        zoneX, = struct.unpack('<i', recv(4))
        zoneY, = struct.unpack('<i', recv(4))
        index, = struct.unpack('<i', recv(4))
        unknownInt, = struct.unpack('<i', recv(4))
        interactionType, = struct.unpack('<H', recv(2))
        unkShort, = struct.unpack('<H', recv(2))

        return ActionPacket(item, zoneX, zoneY, index, unknownInt, interactionType, unkShort)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ActionPacket.pID) )
        packetByteList.append( self.item.Export() )
        packetByteList.append( struct.pack('<i', self.zoneX) )
        packetByteList.append( struct.pack('<i', self.zoneY) )
        packetByteList.append( struct.pack('<i', self.index) )
        packetByteList.append( struct.pack('<i', self.unknownInt) )
        packetByteList.append( struct.pack('<H', self.interactionType) )
        packetByteList.append( struct.pack('<H', self.unkShort) )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
