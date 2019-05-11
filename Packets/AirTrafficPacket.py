import struct
import io
from CubeTypes import Airship
from net import recv2
from .Packet import Packet
class AirTrafficPacket(Packet):
    pID = 0x3
    def __init__(self, airships):
        self.airships = airships
        self.count = len(airships)

    @staticmethod
    def Recv(sock):
        airshipsCount, = struct.unpack('<I', recv2(sock, 4))
        airships = []
        for _ in range(airshipsCount):
            airships += Airship.Import(recv2(sock, 120))
        return AirTrafficPacket(airships)

    def Export(self):
        packet  = struct.pack('<I', pID)
        packet += struct.pack('<I', self.count)
        for ship in self.airships:
            packet += ship.Export()
        return packet

    def Send(self, sock):
        return sock.send(self.Export())
