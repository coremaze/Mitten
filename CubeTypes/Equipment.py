from CubeTypes.Item import Item

class Equipment():
    size = Item.size*13
    def __init__(self,
                 unkItem1 = Item(),
                 necklace = Item(),
                 chest = Item(),
                 feet = Item(),
                 hands = Item(),
                 shoulder = Item(),
                 leftWeapon = Item(),
                 rightWeapon = Item(),
                 leftRing = Item(),
                 rightRing = Item(),
                 light = Item(),
                 special = Item(),
                 pet = Item()):
        self.unkItem1 = unkItem1
        self.necklace = necklace
        self.chest = chest
        self.feet = feet
        self.hands = hands
        self.shoulder = shoulder
        self.leftWeapon = leftWeapon
        self.rightWeapon = rightWeapon
        self.leftRing = leftRing
        self.rightRing = rightRing
        self.light = light
        self.special = special
        self.pet = pet

    @classmethod
    def Import(self, data):
        unkItem1 = Item.Import(data)
        necklace = Item.Import(data)
        chest = Item.Import(data)
        feet = Item.Import(data)
        hands = Item.Import(data)
        shoulder = Item.Import(data)
        leftWeapon = Item.Import(data)
        rightWeapon = Item.Import(data)
        leftRing = Item.Import(data)
        rightRing = Item.Import(data)
        light = Item.Import(data)
        special = Item.Import(data)
        pet = Item.Import(data)

        return Equipment(unkItem1, necklace, chest, feet, hands, shoulder, leftWeapon,
                 rightWeapon, leftRing, rightRing, light, special, pet)

    def Export(self):
        output = self.unkItem1.Export()
        output += self.necklace.Export()
        output += self.chest.Export()
        output += self.feet.Export()
        output += self.hands.Export()
        output += self.shoulder.Export()
        output += self.leftWeapon.Export()
        output += self.rightWeapon.Export()
        output += self.leftRing.Export()
        output += self.rightRing.Export()
        output += self.light.Export()
        output += self.special.Export()
        output += self.pet.Export()
        return output
