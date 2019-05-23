class OnPacket():
    '''
    Triggered when a packet is received.
    
    connection: The Connection receiving the packet
    packet: The Packet which has been received
    fromClient: A bool representing the direction the packet is coming from

    return NO_ACTION or None to have Mitten continue forwarding as normal
    return BLOCK to have Mitten not continue processing the packet
    return MODIFY to have Mitten re-export the packet
    '''
    pass
class OnServerFailure():
    '''
    Triggered when the server refuses a connection.
    '''
    pass

class OnConnect():
    '''
    Triggered when a connection is made.

    connection: The new Connection
    '''
    pass

class OnDisconnect():
    '''
    Triggered when a connection is broken.

    connection: The departing Connection
    '''
    pass

class OnForward():
    '''
    Triggered when a connection to the internal server is about to be made.

    clientSock: The socket of the incoming client
    address: A string containing the IP address of the incoming client
    port: An int representing the port of the incoming client

    return NO_ACTION or None to have Mitten connect to the internal server as normal
    return BLOCK to have Mitten stop processing the connection. You are responsible for closing the client socket, if you need to.
    return a tuple with ('Server address' portNumber) to have Mitten forward to a different server.
    '''

MITTEN_EVENTS = {
    OnPacket: [],
    OnServerFailure: [],
    OnConnect: [],
    OnDisconnect: [],
    OnForward: []
    }

def Handle(eventType):
    global MITTEN_EVENTS
    if eventType not in MITTEN_EVENTS:
        raise ValueError(f'{eventType} is not an event handled by Mitten.')
    def Register(func):
        MITTEN_EVENTS[eventType].append(func)
        return func
    return Register
