class IDContainer():
    MIN_ID = 0x20000000000 #This is deliberately above the range GUID Fix can provide
    def __init__(self):
        self.busy = False
        self._USED_IDS = []
    def GetID(self):
        while self.busy: pass
        self.busy = True
        i = self.MIN_ID
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
            
idContainer = IDContainer()

def GetID():
    return idContainer.GetID()

def FreeID(ID):
    return idContainer.FreeID(ID)
