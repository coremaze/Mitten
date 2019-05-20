from Mitten.Events import *

@Handle(OnConnect)
def ConnectionHandler(connection):
    print(f'{connection.ClientIP()} has connected.')

@Handle(OnDisconnect)
def DisconnectionHandler(connection):
    print(f'{connection.ClientIP()} has disconnected.') 
