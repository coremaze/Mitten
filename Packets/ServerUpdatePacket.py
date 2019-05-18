import struct
import io
from .Packet import Packet
from CubeTypes import Block, Particle, Sound, StaticEntity, Mission, Hit, Drop, Projectile, Pickup, Kill, Damage, PassiveProc
import zlib

class ServerUpdatePacket(Packet):
    pID = 0x4
    def __init__(self, blocks, hits, particles, sounds, projectiles, staticEntities, zoneItems, p48,
                 pickups, kills, damages, passiveProcs, missions):
        self.blocks = blocks
        self.hits = hits
        self.particles = particles
        self.sounds = sounds
        self.projectiles = projectiles
        self.staticEntities = staticEntities
        self.zoneItems = zoneItems
        self.p48 = p48
        self.pickups = pickups
        self.kills = kills
        self.damages = damages
        self.passiveProcs = passiveProcs
        self.missions = missions

    @staticmethod
    def Recv(connection, fromClient):
        recv = [connection.RecvServer, connection.RecvClient][fromClient]
        
        size, = struct.unpack('<I', recv(4))
        zlibData = recv(size)

        data = io.BytesIO(zlib.decompress(zlibData))

##        fulldata = zlib.decompress(zlibData)

        blocks = [Block.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        hits = [Hit.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        particles = [Particle.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        sounds = [Sound.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        projectiles = [Projectile.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        staticEntities = [StaticEntity.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        
        zoneItems = {}
        n = struct.unpack('I', data.read(4))[0]
        for _ in range(n):
            zoneX = struct.unpack('I', data.read(4))[0]
            zoneY = struct.unpack('I', data.read(4))[0]
            if (zoneX, zoneY) not in zoneItems:
                zoneItems[(zoneX, zoneY)] = []
            m = struct.unpack('I', data.read(4))[0]
            zoneItems[(zoneX, zoneY)].extend([Drop.Import(data) for x in range(m)])

        p48 = {}
        n = struct.unpack('I', data.read(4))[0]
        for _ in range(n):
            something = struct.unpack('q', data.read(8))[0]
            if something not in p48:
                p48[something] = []
            m = struct.unpack('I', data.read(4))[0]
            p48[something].extend([data.read(16) for x in range(m)])

##        p48 = []
##        n = struct.unpack('I', data.read(4))[0]
##        for _ in range(n):
##            guid = struct.unpack('q', data.read(8))[0]
##            m = struct.unpack('I', data.read(4))[0]
##            p48.append([data.read(16) for x in range(m)])
##
##        if p48: print(p48)
##
##
##        rest_of_data = data.read(100000)
##
##        taken_size = len(fulldata) - len(rest_of_data)
##
##
##        import random
##        p48_header = b'\x01\x02\x03\x04' * 2
##        
##        test_p48s = [b'\x01'*16]*2
##        p48_size = struct.pack('<I', len(test_p48s))
##        
##        new_data = (fulldata[:taken_size]
##        + b'\x02\x00\x00\x00'
##        + p48_header
##        + p48_size
##        + b''.join(test_p48s)
##
##        + p48_header
##        + p48_size
##        + b''.join(test_p48s)
##        
##        + fulldata[taken_size+4:])
##        zlibData = zlib.compress(new_data)

            
        pickups = [Pickup.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        kills = [Kill.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        damages = [Damage.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        passiveProcs = [PassiveProc.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]
        missions = [Mission.Import(data) for x in range(struct.unpack('I', data.read(4))[0])]

        return ServerUpdatePacket(blocks, hits, particles, sounds, projectiles, staticEntities, zoneItems, p48,
                 pickups, kills, damages, passiveProcs, missions)

    def Export(self, toServer):
        packetByteList = []
        packetByteList.append( struct.pack('<I', ServerUpdatePacket.pID) )

        zlibDataList = []
        zlibDataList.append( struct.pack('<I', len(self.blocks)) )
        zlibDataList.extend( [x.Export() for x in self.blocks] )

        zlibDataList.append( struct.pack('<I', len(self.hits)) )
        zlibDataList.extend( [x.Export() for x in self.hits] )

        zlibDataList.append( struct.pack('<I', len(self.particles)) )
        zlibDataList.extend( [x.Export() for x in self.particles] )

        zlibDataList.append( struct.pack('<I', len(self.sounds)) )
        zlibDataList.extend( [x.Export() for x in self.sounds] )

        zlibDataList.append( struct.pack('<I', len(self.projectiles)) )
        zlibDataList.extend( [x.Export() for x in self.projectiles] )

        zlibDataList.append( struct.pack('<I', len(self.staticEntities)) )
        zlibDataList.extend( [x.Export() for x in self.staticEntities] )

        zlibDataList.append( struct.pack('<I', len(self.zoneItems)) )
        for (zoneX, zoneY) in self.zoneItems:
            items = self.zoneItems[(zoneX, zoneY)]
            zlibDataList.append( struct.pack('<I', zoneX) )
            zlibDataList.append( struct.pack('<I', zoneY) )
            zlibDataList.append( struct.pack('<I', len(items)) )
            zlibDataList.extend( [x.Export() for x in items] )

        zlibDataList.append( struct.pack('<I', len(self.p48)) )
        for something in self.p48:
            items = self.p48[something]
            zlibDataList.append( struct.pack('<I', something) )
            zlibDataList.append( struct.pack('<I', len(items)) )
            zlibDataList.extend( items )

        zlibDataList.append( struct.pack('<I', len(self.pickups)) )
        zlibDataList.extend( [x.Export() for x in self.pickups] )

        zlibDataList.append( struct.pack('<I', len(self.kills)) )
        zlibDataList.extend( [x.Export() for x in self.kills] )

        zlibDataList.append( struct.pack('<I', len(self.damages)) )
        zlibDataList.extend( [x.Export() for x in self.damages] )

        zlibDataList.append( struct.pack('<I', len(self.passiveProcs)) )
        zlibDataList.extend( [x.Export() for x in self.passiveProcs] )

        zlibDataList.append( struct.pack('<I', len(self.missions)) )
        zlibDataList.extend( [x.Export() for x in self.missions] )

        zlibData = zlib.compress(b''.join(zlibDataList))


        packetByteList.append(struct.pack('<I', len(zlibData)))
        packetByteList.append(zlibData)
        
        return b''.join(packetByteList)

    def Send(self, connection, toServer):
        send = [connection.SendClient, connection.SendServer][toServer]
        return send(self.Export(toServer))
