class Packet():
    @staticmethod
    def Recv(connection, fromClient):
        raise NotImplemented("Method must be implemented")
    def Export(self, toServer):
        raise NotImplemented("Method must be implemented")
    def Send(self, connection, toServer):
        raise NotImplemented("Method must be implemented")
