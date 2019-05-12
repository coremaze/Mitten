import struct
import io
from .Packet import Packet
class ChatPacket(Packet):
    pID = 0xA
    def __init__(self, message, entityID=None):
        self.message = message
        self.entityID = entityID

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        if not fromClient:
            entityID, = struct.unpack('<q', recv(8))
            
        messageLength, = struct.unpack('<I', recv(4))
        message  = recv(messageLength*2).decode('utf-16le')
        
        if fromClient:
            return ChatPacket(message)
        else:
            return ChatPacket(message, entityID=entityID)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ChatPacket.pID) )
        if not toServer:
            packetByteList.append( struct.pack('<q', self.entityID) )
        packetByteList.append( struct.pack('<I', len(self.message)) )
        packetByteList.append(self.message.encode('utf-16le') )
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
