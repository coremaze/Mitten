#https://stackoverflow.com/questions/1057431

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and basename(f)[:-3] not in ('__init__', 'Packet')]
from . import *
classes = [getattr(globals()[x], x) for x in __all__]

