import struct
class StatMultipliers():
    size = 20
    def __init__(self, HPMultiplier, attackSpeedMultiplier, damageMultiplier, armorMultiplier, resistanceMultiplier):
        self.HPMultiplier = HPMultiplier
        self.attackSpeedMultiplier = attackSpeedMultiplier
        self.damageMultiplier = damageMultiplier
        self.armorMultiplier = armorMultiplier
        self.resistanceMultiplier = resistanceMultiplier
    @classmethod
    def Import(self, data):
        HPMultiplier, = struct.unpack('<f', data.read(4))
        attackSpeedMultiplier, = struct.unpack('<f', data.read(4))
        damageMultiplier, = struct.unpack('<f', data.read(4))
        armorMultiplier, = struct.unpack('<f', data.read(4))
        resistanceMultiplier, = struct.unpack('<f', data.read(4))

        return StatMultipliers(HPMultiplier, attackSpeedMultiplier, damageMultiplier, armorMultiplier, resistanceMultiplier)
    def Export(self):
        output = struct.pack('<f', self.HPMultiplier)
        output += struct.pack('<f', self.attackSpeedMultiplier)
        output += struct.pack('<f', self.damageMultiplier)
        output += struct.pack('<f', self.armorMultiplier)
        output += struct.pack('<f', self.resistanceMultiplier)

        return output