from Mitten.Constants import *
from Packets import *
from Plugins.IgnoreBan import aBannedConnections, banner
from Mitten.Events import *

# Currently Implemented:
# Bad Item banner
# Script banner

aHandlers = {}
aWaitingForEntUpdate = {}  # Monitored to see if they send entity update packet or not
aRules = {
    'dropBadItem': lambda packet: (packet.interactionType is 6 and ITEM_NAMES.get((packet.item.itemType, packet.item.subType)) is 'Bait')
}

def BanConnection(connection, reason):
    global aWaitingForEntUpdate

    print(f'Anticheat Banned {connection.ClientIP()} for {reason}.')
    del aWaitingForEntUpdate[connection]
    aBannedConnections[connection] = True
    banner.Ban(connection.ClientIP())
    connection.Close()

def HandleGenericPacket(connection, packet):
    if connection in aWaitingForEntUpdate:
        BanConnection(connection, 'never sending entity update')
        return BLOCK
    return

def HandleVersionPacket(connection, packet):
    global aWaitingForEntUpdate

    aMonitoredIPs = [x for x in aWaitingForEntUpdate if x.ClientIP() == connection.ClientIP()]
    if len(aMonitoredIPs) > 0:
        BanConnection(aMonitoredIPs[0], 'multiple fake connections')
        return BLOCK
    aWaitingForEntUpdate[connection] = True
    return

def HandleEntityUpdatePacket(connection, packet):
    global aWaitingForEntUpdate

    if connection in aWaitingForEntUpdate:
        del aWaitingForEntUpdate[connection]
    return

def HandleActionPacket(connection, packet):
    if True in (aRules['dropBadItem'](packet),):
        BanConnection(connection, 'dropping a bad item')

    return

@Handle(OnPacket)
def HandlePacket(connection, packet, fromClient):
    if not fromClient: return
    return aHandlers.get(type(packet).pID, HandleGenericPacket)(connection, packet)


aHandlers[ActionPacket.pID] = HandleActionPacket
aHandlers[VersionPacket.pID] = HandleVersionPacket
aHandlers[EntityUpdatePacket.pID] = HandleEntityUpdatePacket

