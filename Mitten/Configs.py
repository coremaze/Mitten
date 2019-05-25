import json

CONFIG = {}

def LoadConfig():
    global CONFIG
    while True:
        try:
            with open('config.json', 'r') as f:
                data = f.read().strip()
        except FileNotFoundError:
            with open('config.json', 'w') as f:
                pass
        else:
            break
    if not data:
        data = '{}'
    CONFIG = json.loads(data)
    

def SaveConfig():
    while True:
        try:
            with open('config.json', 'w') as f:
                f.write(json.dumps(CONFIG, indent=4))
        except: pass
        else: break
        
def PluginName(plugin):
    if type(plugin) != str:
        string = plugin.__name__.split('.')[0]
    else:
        string = plugin
    return string

def LoadPlugin(plugin):
    string = PluginName(plugin)
    if string not in CONFIG:
        CONFIG[string] = {'enabled': True}
    SaveConfig()

def GetAttribute(plugin, attribute, default=None):
    string = PluginName(plugin)
    if attribute not in CONFIG[string]:
        SetAttribute(plugin, attribute, default)
    return CONFIG[string][attribute]

def SetAttribute(plugin, attribute, value):
    string = PluginName(plugin)
    CONFIG[string][attribute] = value
    SaveConfig()
    
