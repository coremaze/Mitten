from Packets import *
from Mitten.Constants import *
from Mitten.Events import *
import time

class Banner():
    def __init__(self):
        self.lastUpdate = 0
        self.IPs = []
        self.Update()

    def Update(self):
        self.lastUpdate = time.time()
        while True:
            try:
                with open('bans.txt', 'r') as f:
                    IPs = [x.strip() for x in f.read().split('\n') if x.strip()]
            except FileNotFoundError:
                with open('bans.txt', 'w') as f:
                    pass
            else:
                break
        self.IPs = IPs

    def IsBanned(self, IP):
        UPDATE_TIME = 5.0
        if time.time() - self.lastUpdate > UPDATE_TIME:
            self.Update()
        return IP in self.IPs

    def Ban(self, IP):
        self.IPs.append(IP)
        while True:
            try:
                with open('bans.txt', 'a+') as f:
                    f.write(f'\n{IP}\n')
            except FileNotFoundError:
                with open('bans.txt', 'w') as _:
                    pass
            else:
                break



class Holder():
    holders = []
    def __init__(self, connection):
        self.holders.append(self)
        self.connection = connection
        self.gotClient = False

    def HoldClient(self):
        self.gotClient = True
        #Recv their garbage until they go away
        while not self.connection.closed:
            self.connection.RecvClient(4)
        self.gotClient = False

    def HoldServer(self):
        #Close the server socket, but also don't return until the client leaves
        while not self.gotClient: time.sleep(0.01)
        self.connection.serverSock.close()
        while self.gotClient: time.sleep(0.01)

        
aBannedConnections = {}
banner = Banner()
@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    global banner
    IP = connection.ClientIP()
    # If not banned but not visited yet
    if banner.IsBanned(IP) and aBannedConnections.get(connection, False) is False:
        aBannedConnections[connection] = True
        print(f'{IP} Is banned and thinks we care about his packets')
        
    # If visited
    if aBannedConnections.get(connection, False) is True:
        # Hold current connection
        if connection not in [x.connection for x in Holder.holders]:
            Holder(connection)
        holder = [x for x in Holder.holders if x.connection == connection][0]
        
        if fromClient:
            # Send a versionpacket just to make sure the loser gets his join packet
            # We can't allow the client to do this on their own because they could
            # spam version packets
            VersionPacket(3).Send(connection, toServer=True)
            holder.HoldClient()
            return BLOCK
        else:
            #Stop the server's connection once the server acknowledges the client
            if type(packet) != JoinPacket:
                holder.HoldServer()

