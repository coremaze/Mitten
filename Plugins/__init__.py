#https://stackoverflow.com/questions/1057431

from os.path import dirname, basename, isfile, join
import glob
import Mitten.Configs

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and basename(f)[:-3] not in ('__init__', 'Packet')]

#Load configs for plugins, and the plugins which are enabled.
Mitten.Configs.LoadConfig()
pluginList = []
for pluginName in __all__:
    Mitten.Configs.LoadPlugin(pluginName)
    if Mitten.Configs.GetAttribute(pluginName, 'enabled'):
        print(f'Loading plugin {pluginName}')
        __import__('Plugins.'+pluginName)
        pluginList.append(globals()[pluginName])
    else:
        print(f'NOT loading plugin {pluginName}')
