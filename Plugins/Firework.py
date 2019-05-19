from Packets.ServerUpdatePacket import ServerUpdatePacket
from Packets.EntityUpdatePacket import EntityUpdatePacket
from Packets.ChatPacket import ChatPacket
from CubeTypes.FloatVector3 import FloatVector3
from CubeTypes.IntVector3 import IntVector3
from CubeTypes.LongVector3 import LongVector3
from CubeTypes import Particle
from CubeTypes import Sound
from CubeTypes import StaticEntity
from CubeTypes import Spirit
from CubeTypes import Item
from CubeTypes import Equipment
from CubeTypes import Appearance
from Mitten.Constants import *
from random import uniform as r
from threading import Thread
import time

connections = []
fireworkID = 10000
def FireworkThread(position):
    global connections, fireworkID
    position = LongVector3(position.x, position.y, position.z)
    time.sleep(3)
    cons = connections[:]

    #the position to make the rocket noise at
    pshpos = FloatVector3(position.x/65536,
                          position.y/65536,
                          position.z/65536 + 3)

    sup = ServerUpdatePacket([],[],[
        #the rocket particle
        Particle(position, FloatVector3(0.0,0.0,60.0), 0.9, 0.1, 0.1, 1.0,
                                0.75, 1, 0, 0.0, 0)
        ],[
        #the sound the rocket makes
        Sound(pshpos, 37, 2, 1.0)
        ],[],[],{},{},[],[],[],[],[])

    #send the rocket and noise to everyone
    for c in cons:
        try: Thread(target=sup.Send, args=[c, False]).start()
        except: pass

    #time before it explodes
    time.sleep(1)

    #Explode in the sky instead of at the ground
    position.z += 65536 * 50

    #where the explosion noise will come from
    boompos = FloatVector3(position.x/65536,
                           position.y/65536,
                           position.z/65536)

               
    
    sup = ServerUpdatePacket([],[],[
        #the colored particles
        Particle(position, FloatVector3(0.0,0.0,1.0), r(0.3, 0.9), r(0.3, 0.9), r(0.3, 0.9), 1.0,
                                0.25, 600, 0, 30.0, 0),
        #the fire particles
        Particle(position, FloatVector3(0.0,0.0,1.0), 1.0, 1.0, 1.0, 1.0,
                                0.15, 50, 1, 20.0, 0)
        ],[
        #The boom is made from many layered sound effects
        Sound(boompos, 19, 0.1, 7.0),
        Sound(boompos, 19, 0.2, 6.0),
        Sound(boompos, 19, 0.3, 5.0),
        Sound(boompos, 19, 0.4, 4.0),
        Sound(boompos, 19, 0.5, 3.0),
        Sound(boompos, 25, 0.5, 0.3)
        ],[],[],{},{},[],[],[],[],[])


    #Constuct the entity which will be holding the light source
    equipList = [Item(24, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, [Spirit(0, 0, 0, 0, 0, 0) for i in range(32)], 0) for _ in range(13)]
    appearance = Appearance(0, 0, 0, 0, 0, 0, 0, FloatVector3(0.0, 0.0, 0.0),
                 1, 1, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, FloatVector3(0.0, 0.0, 0.0),
                 FloatVector3(0.0, 0.0, 0.0), FloatVector3(0.0, 0.0, 0.0), FloatVector3(0.0, 0.0, 0.0), FloatVector3(0.0, 0.0, 0.0), FloatVector3(0.0, 0.0, 0.0))
    
    this_id, fireworkID = fireworkID, fireworkID+1
    p = EntityUpdatePacket(this_id, {'position': position,
                                    'equipment': Equipment(*equipList),
                                    'creatureFlags': 0xFFFF,
                                    'appearance': appearance,
                                    'name': 'Firework'})
    
    #send noise and particles to everyone
    for c in cons:
        Thread(target=sup.Send, args=[c, False]).start()

    #send and update the light source
    for rarity in range(13, -1, -1):
        p.fields['equipment'].light.rarity = rarity
        #exporting the raw data manually is an optimization for speed
        raw_data = p.Export(False)
        init_time = time.time()
        while time.time() - init_time < 0.20:
            for c in cons:
                Thread(target=c.SendClient, args=[raw_data]).start()
            time.sleep(0.001)

    
def Firework(position):
    Thread(target=FireworkThread, args=[position]).start()

positions = {}
def HandlePacket(connection, packet, fromClient):
    global connections, positions, dummyDelta
    if connection not in connections:
        connections.append(connection)
    connections = [x for x in connections if not x.closed]
    if type(packet) == EntityUpdatePacket and fromClient:
        if 'position' in packet.fields:
            position = packet.fields['position']
            positions[connection] = position
            for c in list(positions):
                if c.closed:
                    del positions[c]
    elif type(packet) == ChatPacket and fromClient:
        if packet.message == 'f' and connection in positions:
            Firework(positions[connection])
            return BLOCK
