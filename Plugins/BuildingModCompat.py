import struct
import io
from Packets import Packet
from Mitten.Events import *

ZONE_LOAD_PACKET = 1
ZONE_UNLOAD_PACKET = 2
BLOCK_PLACE_PACKET = 3

class BuildingModPacket(Packet):
    pID = 1263488066
    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        subID, = struct.unpack('<I', recv(4))
        if subID == ZONE_LOAD_PACKET:
            return BuildingModZoneLoadPacket.Recv(connection, fromClient)
        if subID == ZONE_UNLOAD_PACKET:
            return BuildingModZoneUnloadPacket.Recv(connection, fromClient)
        if subID == BLOCK_PLACE_PACKET:
            return BuildingModBlockPlacePacket.Recv(connection, fromClient)
        raise Exception(f'Bad Building Mod Packet: {subID}')

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))

class BuildingModZoneLoadPacket(BuildingModPacket):
    pID = ZONE_LOAD_PACKET
    def __init__(self, zoneX, zoneY):
        self.zoneX = zoneX
        self.zoneY = zoneY
        #print(f'Loaded {zoneX}, {zoneY}')

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        zoneX, = struct.unpack('<I', recv(4))
        zoneY, = struct.unpack('<I', recv(4))
        return BuildingModZoneLoadPacket(zoneX, zoneY)

    def Export(self, toServer):
        dataList = []
        dataList.append( struct.pack('<I', BuildingModPacket.pID) )
        dataList.append( struct.pack('<I', BuildingModZoneLoadPacket.pID) )
        dataList.append( struct.pack('<I', self.zoneX) )
        dataList.append( struct.pack('<I', self.zoneY) )
        return b''.join(dataList)

class BuildingModZoneUnloadPacket(BuildingModPacket):
    pID = ZONE_UNLOAD_PACKET
    def __init__(self, zoneX, zoneY):
        self.zoneX = zoneX
        self.zoneY = zoneY
        #print(f'Unoaded {zoneX}, {zoneY}')

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        zoneX, = struct.unpack('<I', recv(4))
        zoneY, = struct.unpack('<I', recv(4))
        return BuildingModZoneUnloadPacket(zoneX, zoneY)

    def Export(self, toServer):
        dataList = []
        dataList.append( struct.pack('<I', BuildingModPacket.pID) )
        dataList.append( struct.pack('<I', BuildingModZoneUnloadPacket.pID) )
        dataList.append( struct.pack('<I', self.zoneX) )
        dataList.append( struct.pack('<I', self.zoneY) )
        return b''.join(dataList)

class BuildingModBlockPlacePacket(BuildingModPacket):
    pID = BLOCK_PLACE_PACKET
    def __init__(self, x, y, z, r, g, b, blockType):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        self.blockType = blockType
        #print(f'block {(x,y,z,r,g,b,blockType)}')

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        x, = struct.unpack('<I', recv(4))
        y, = struct.unpack('<I', recv(4))
        z, = struct.unpack('<i', recv(4))
        r, = struct.unpack('<B', recv(1))
        g, = struct.unpack('<B', recv(1))
        b, = struct.unpack('<B', recv(1))
        blockType, = struct.unpack('<B', recv(1))
        return BuildingModBlockPlacePacket(x, y, z, r, g, b, blockType)

    def Export(self, toServer):
        dataList = []
        dataList.append( struct.pack('<I', BuildingModPacket.pID) )
        dataList.append( struct.pack('<I', BuildingModBlockPlacePacket.pID) )
        dataList.append( struct.pack('<I', self.x) )
        dataList.append( struct.pack('<I', self.y) )
        dataList.append( struct.pack('<i', self.z) )
        dataList.append( struct.pack('<B', self.r) )
        dataList.append( struct.pack('<B', self.g) )
        dataList.append( struct.pack('<B', self.b) )
        dataList.append( struct.pack('<B', self.blockType) )
        return b''.join(dataList)

@Handle(OnUnknownPacket)
def HandleUnknownPacket(connection, pID, fromClient):
    if pID == BuildingModPacket.pID:
        return BuildingModPacket
