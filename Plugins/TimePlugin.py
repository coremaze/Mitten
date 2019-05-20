from Packets.ChatPacket import ChatPacket
from Packets.TimePacket import TimePacket
from Mitten.Constants import *
from Mitten.Events import *

custom_times = {}

@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    if type(packet) == ChatPacket:
        return HandleChatPacket(connection, packet, fromClient)
    if type(packet) == TimePacket:
        return HandleTimePacket(connection, packet, fromClient)

    
def HandleTimePacket(connection, packet, fromClient):
    if connection not in custom_times: return
    packet.time = custom_times[connection]
    return MODIFY
    
    
def HandleChatPacket(connection, packet, fromClient):
    if not fromClient: return
    if packet.message.lower() == '!time unset':
        if connection not in custom_times: return
        del custom_times[connection]
        newPacket = ChatPacket(f'Time has been unset. (But only for you!)', 0)
        newPacket.Send(connection, toServer=False)
        return BLOCK
    
    args = packet.message.lower().split(' ')
    if len(args) != 3: return
    if args[0] != '!time': return
    if args[1] != 'set': return
    time = args[2].split(':')
    if len(time) != 2: return
    try:
        hours, minutes = int(time[0])%24, int(time[1])%60
    except:
        return

    mseconds = hours * 3600000 + minutes * 60000

    newPacket = ChatPacket(f'Time has been set to {hours}:{minutes:02d}. (But only for you!)', 0)
    newPacket.Send(connection, toServer=False)

    custom_times[connection] = mseconds

    return BLOCK
    
    
