class Packet():
    @staticmethod
    def Import(self, data):
        raise NotImplemented("Method must be implemented")
    def Export(self):
        raise NotImplemented("Method must be implemented")
    def Send(self, sock):
        raise NotImplemented("Method must be implemented")
