from Packets.EntityUpdatePacket import EntityUpdatePacket
from Packets.AirTrafficPacket import AirTrafficPacket

#return a true value to disallow packet from being further processed
def HandlePacket(connection, packet, fromClient):
    if type(packet) in (EntityUpdatePacket, AirTrafficPacket):
        return
    if not fromClient:
        return
    
    print(packet)

    
    

