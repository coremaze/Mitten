import struct
import io
from CubeTypes import Airship
class AirTrafficPacket():
    pID = 0x3
    def __init__(self, airships):
        self.airships = airships
        self.count = len(airships)

    @staticmethod
    def Import(data):
        dID, = struct.unpack('<I', data.read(4))
        if (AirTrafficPacket.pID is not dID) :
            raise ValueError(f'Received packet ID of {dID} when {AirTrafficPacket.pID} was expected.')

        airshipsCount, = struct.unpack('<I', data.read(4))
        airships = []
        for _ in range(airshipsCount):
            airships += Airship.Import(data.read(120))
        
        return AirTrafficPacket(airships)

    def Export(self):
        packet  = struct.pack('<I', pID)
        packet += struct.pack('<I', self.count)
        for ship in self.airships:
            packet += ship.Export()
        return packet

    def Send(self, sock):
        return sock.send(self.Export())
