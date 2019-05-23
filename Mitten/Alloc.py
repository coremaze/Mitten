class IDContainer():
    def __init__(self, minID):
        self.busy = False
        self._USED_IDS = []
        self.minID = minID
    def GetID(self):
        while self.busy: pass
        self.busy = True
        i = self.minID
        while True:
            if i not in self._USED_IDS:
                self._USED_IDS.append(i)
                self.busy = False
                return i
            i += 1

    def FreeID(self, ID):
        while self.busy: pass
        self.busy = True
        if ID in self._USED_IDS:
            self._USED_IDS.remove(ID)
        self.busy = False
            
GUIDContainer = IDContainer(0x20000000000) #This is deliberately above the range GUID Fix can provide

def GetGUID():
    return GUIDContainer.GetID()

def FreeGUID(ID):
    return GUIDContainer.FreeID(ID)
