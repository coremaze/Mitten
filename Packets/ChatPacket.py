import struct
import io
from net import recv2
from .Packet import Packet
class ChatPacket(Packet):
    pID = 0xA
    def __init__(self, message):
        self.message = message

    @staticmethod
    def Recv(sock):
        messageLength, = struct.unpack('<I', recv2(sock, 4))
        message  = recv2(sock, messageLength*2).decode('utf-16le')
        return ChatPacket(message)

    def Export(self):
        packet  = struct.pack('<I', pID)
        packet += struct.pack('<I', len(self.message))
        packet += self.message.encode('utf-16le')
        return packet

    def Send(self, sock):
        return sock.send(self.Export())
