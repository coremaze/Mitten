from .ActionPacket import ActionPacket
from .AirTrafficPacket import AirTrafficPacket
from .ChatPacket import ChatPacket
from .CreatureUpdateFinishedPacket import CreatureUpdateFinishedPacket
from .CreatureUpdatePacket import CreatureUpdatePacket
from .HitPacket import HitPacket
from .JoinPacket import JoinPacket
from .MapSeedPacket import MapSeedPacket
from .Packet import Packet
from .PassiveProcPacket import PassiveProcPacket
from .RegionDiscoveredPacket import RegionDiscoveredPacket
from .ServerFullPacket import ServerFullPacket
from .ServerUpdatePacket import ServerUpdatePacket
from .ShootPacket import ShootPacket
from .TimePacket import TimePacket
from .VersionPacket import VersionPacket
from .ZoneDiscoveredPacket import ZoneDiscoveredPacket

classes = [ActionPacket, AirTrafficPacket, ChatPacket,
           CreatureUpdateFinishedPacket, CreatureUpdatePacket,
           HitPacket, JoinPacket, MapSeedPacket, PassiveProcPacket,
           RegionDiscoveredPacket, ServerFullPacket, ServerUpdatePacket,
           ShootPacket, TimePacket, VersionPacket, ZoneDiscoveredPacket]
