#https://stackoverflow.com/questions/1057431

from os.path import dirname, basename, isfile, join
import glob
_modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in _modules if isfile(f) and basename(f)[:-3] not in ('__init__', 'Packet') and ' ' not in basename(f)[:-3] and '\t' not in basename(f)[:-3]]
for packetName in __all__:
    exec(f'from .{packetName} import {packetName}') #sorry
classes = [globals()[x] for x in __all__]
