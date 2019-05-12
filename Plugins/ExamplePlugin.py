from Packets.ChatPacket import ChatPacket

#return a true value to disallow packet from being further processed
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
        return True

    #You can send new packets
    if not fromClient and 'hello' in packet.message.lower():
        newPacket = ChatPacket('Hello!', 0)
        newPacket.Send(connection, fromClient)

    
    
