import struct
import io
from net import recv2
from .Packet import Packet
class ChatPacket(Packet):
    pID = 0xA
    #Client->Server
    def __init__(self, message):
        self.message = message
        self.entityID = 0

    #Server->Client
    def __init__(self, entityID, message):
        self.message = message
        self.entityID = entityID

    @staticmethod
    def Recv(self, connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        if not fromClient:
            entityID = struct.unpack('<q', recv(8))
            
        messageLength, = struct.unpack('<I', recv(4))
        message  = recv(messageLength*2).decode('utf-16le')
        
        if fromClient:
            return ChatPacket(message)
        else:
            return ChatPacket(entityID, message)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ChatPacket.pID) )
        if toServer:
            packetByteList.append( struct.pack('<q', self.entityID) )
        packetByteList.append( struct.pack('<I', len(self.message)) )
        packetByteList.append(self.message.encode('utf-16le') )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
