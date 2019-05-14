from Packets.JoinPacket import JoinPacket
from Packets.ChatPacket import ChatPacket
from Packets.ActionPacket import ActionPacket
import time

action_packet_stacks = {}

def BanIP(IP):
    while True:
        try:
            with open('bans.txt', 'a') as f:
                f.write(f'\n{IP}\n')
        except FileNotFoundError:
            with open('bans.txt', 'w') as f:
                pass
        else:
            break

def HandlePacket(connection, packet, fromClient):
    if not fromClient:
        return
    
    if connection not in action_packet_stacks:
        action_packet_stacks[connection] = []
        
    #Remove old records
    to_close = []
    for conn in action_packet_stacks:
        if conn.closed:
            to_close.append(conn)
    for conn in to_close:
        del action_packet_stacks[conn]

        
    if type(packet) == JoinPacket:
        return HandleJoinPacket(connection, packet, fromClient)
    if type(packet) == ActionPacket:
        return HandleActionPacket(connection, packet, fromClient)



def HandleJoinPacket(connection, packet, fromClient):
    pass
    
def HandleActionPacket(connection, packet, fromClient):
    curTime = time.time()
    action_packet_stacks[connection].append(curTime)
    if len(action_packet_stacks[connection]) > 500:
        action_packet_stacks[connection].pop(0)

    #last 6 seconds
    recentActions = sum([1 for x in action_packet_stacks[connection] if (curTime - x) < 6])
    #print(f'{recentActions} recent actions')

    #last 60 seconds
    lessRecentActions = sum([1 for x in action_packet_stacks[connection] if (curTime - x) < 60])
    #print(f'{lessRecentActions} less recent actions')

    
    if recentActions >= 100 or lessRecentActions >= 420:
        IP = connection.ClientIP()
        BanIP(IP)
        print(f'Banning {IP}. They sent {recentActions} actions in the last 6 seconds, and {lessRecentActions} actions in the last 60 seconds.')
        connection.Close()
        return True
