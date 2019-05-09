import struct
class AirTrafficPacket():
    def __init__(self, airships):
        self.airships = airships
    @staticmethod
    def Import(data):
        raise NotImplemented("Method must be implemented")
    def Export(self):
        raise NotImplemented("Method must be implemented")
    def Send(self, sock):
        raise NotImplemented("Method must be implemented")

