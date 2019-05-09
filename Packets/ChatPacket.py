import struct
import io
class ChatPacket():
    pID = 0xA
    def __init__(self, message):
        self.message = message
    # Removed the 'self' parameter from Import because it's static
    @staticmethod
    def Import(data):
        dID, = struct.unpack('<I', data.read(4))
        if (ChatPacket.pID is not dID) :
            raise ValueError(f'Received packet ID of {dID} when {ChatPacket.pID} was expected.')

        messageLength, = struct.unpack('<I', data.read(4))
        # Multiplying by 2 because each character uses 2 bytes
        message  = data.read(messageLength*2).decode('utf-16le')
        return ChatPacket(message)

    def Export(self):
        packet  = struct.pack('<I', pID)
        packet += struct.pack('<I', len(self.message))
        packet += self.message.encode('utf-16le')
        return packet

    def Send(self, sock):
        return sock.send(self.Export())
