class OnPacket():
    '''
    Triggered when a packet is received.
    
    connection: The Connection receiving the packet
    packet: The Packet which has been received
    fromClient: A bool representing the direction the packet is coming from
    '''
    pass
class OnServerFailure():
    '''
    Triggered the server refuses a connection.
    '''
    pass

class OnConnect():
    '''
    Triggered the server refuses a connection.

    connection: The new Connection
    '''
    pass

class OnDisconnect():
    '''
    Triggered the server refuses a connection.

    connection: The departing Connection
    '''
    pass

MITTEN_EVENTS = {
    OnPacket: [],
    OnServerFailure: [],
    OnConnect: [],
    OnDisconnect: []
    }

def Handle(eventType):
    global MITTEN_EVENTS
    if eventType not in MITTEN_EVENTS:
        raise ValueError(f'{eventType} is not an event handled by Mitten.')
    def Register(func):
        MITTEN_EVENTS[eventType].append(func)
        return func
    return Register
