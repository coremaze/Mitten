from Mitten.Events import *
from Mitten.Constants import *

@Handle(OnForward)
def Forward(clientSock, address, port):
    pass
##    print(clientSock, address, port)

#You may block an incoming connection like this:
##    clientSock.close()
##    return BLOCK
#You may specify a new internal server like this:
    return ('play.cubehaven.com', 12345)
