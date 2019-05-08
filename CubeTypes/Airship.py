import struct
from ..CubeTypes import LongVector3
class Airship():
    def __init__(self, ID, position, velocity, rotation, station, pathRotation, destination, flightState):
        self.id = ID
        self.position = position
        self.velocity = velocity
        self.rotation = rotation
        self.station = station
        self.pathRotation = pathRotation
        self.destination = destination
        self.flightState = flightState
    @classmethod
    def Import(self, data):
        pos = 0
        self.id = struct.unpack("<q", data[pos : pos+8]); pos += 8
        struct.unpack("<I", data[pos : pos+4]); pos += 4 #unknown
        struct.unpack("<I", data[pos : pos+4]); pos += 4 #unknown
        self.position = LongVector3.Import(data[pos : pos + LongVector3.size]); pos += LongVector3.size
        #not complete
    
