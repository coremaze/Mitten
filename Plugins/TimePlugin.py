from Packets.ChatPacket import ChatPacket
from Packets.TimePacket import TimePacket

custom_times = {}

def HandlePacket(connection, packet, fromClient):
    if type(packet) == ChatPacket:
        return HandleChatPacket(connection, packet, fromClient)
    if type(packet) == TimePacket:
        return HandleTimePacket(connection, packet, fromClient)

    
def HandleTimePacket(connection, packet, fromClient):
    if connection not in custom_times: return
    packet.time = custom_times[connection]
    
    
def HandleChatPacket(connection, packet, fromClient):
    if not fromClient: return
    if packet.message.lower() == '!time unset':
        del custom_times[connection]
        newPacket = ChatPacket(f'Time has been unset. (But only for you!)', 0)
        newPacket.Send(connection, fromClient)
        return True
    
    args = packet.message.lower().split(' ')
    if len(args) != 3: return
    if args[0] != '!time': return
    if args[1] != 'set': return
    time = args[2].split(':')
    if len(time) != 2: return
    try:
        hours, minutes = int(time[0]), int(time[1])
    except:
        return

    mseconds = hours * 3600000 + minutes * 60000

    newPacket = ChatPacket(f'Time has been set to {hours}:{minutes:02d}. (But only for you!)', 0)
    newPacket.Send(connection, fromClient)

    custom_times[connection] = mseconds

    return True
    
    
