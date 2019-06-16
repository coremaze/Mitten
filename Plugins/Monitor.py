# Imports
from Packets import VersionPacket
from Mitten.Constants import *
from Mitten.Events import *


from CubeTypes import *
import json

# Variable Definitions

aConnections = []
aHandlers = {}

def canDict(obj):
    try:
        somth = obj.__dict__
        return str(somth)
    except:
        return str(obj)

# Function Definitions & Implementations

def HandleGenericPacket(connection, packet, fromClient):
    if not type(packet) in ( VersionPacket, ):
        return
    #if not fromClient: return
    sPrefix = ["[FROM SERVER]", "[FROM CLIENT]"][fromClient]
    print(f'{sPrefix} {json.dumps( {type(packet).__name__: packet.__dict__}, default=canDict  )}')


                                                    
# Packet event - called every time a packet is received.
@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    return aHandlers.get(type(packet).pID, HandleGenericPacket)(connection, packet, fromClient)
    
# Variable Implementations
    

