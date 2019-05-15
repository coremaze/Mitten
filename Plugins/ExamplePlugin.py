from Packets.ChatPacket import ChatPacket
from Mitten.Constants import *

#return BLOCK to cancel processing of the packet
#return MODIFY if you wish to change a packet
#return None or NO_ACTION if you wish to do neither
def HandlePacket(connection, packet, fromClient):
    #You can use the pID if you want
##    if packet.pID != 10:
##        return

    #Or you can do this
    if type(packet) != ChatPacket:
        return
    
    #You can access attributes of a packet
    print(packet.message)

    #You can change attributes of a packet
    packet.message = packet.message.replace('fuck', '****')

    #You can stop a packet from being processed any further
    if 'shit' in packet.message:
        return BLOCK

    #You can send new packets
    if not fromClient and 'hello' in packet.message.lower():
        newPacket = ChatPacket('Hello!', 0)
        newPacket.Send(connection, fromClient)

    return MODIFY

    
    
