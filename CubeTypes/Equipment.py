from CubeTypes.Item import Item

class Equipment():
    size = Item.size*13
    def __init__(self,
                 unkItem1 = None,
                 necklace = None,
                 chest = None,
                 feet = None,
                 hands = None,
                 shoulder = None,
                 leftWeapon = None,
                 rightWeapon = None,
                 leftRing = None,
                 rightRing = None,
                 light = None,
                 special = None,
                 pet = None):

        if unkItem1 is None: unkItem1 = Item()
        if necklace is None: necklace = Item()
        if chest is None: chest = Item()
        if feet is None: feet = Item()
        if hands is None: hands = Item()
        if shoulder is None: shoulder = Item()
        if leftWeapon is None: leftWeapon = Item()
        if rightWeapon is None: rightWeapon = Item()
        if leftRing is None: leftRing = Item()
        if rightRing is None: rightRing = Item()
        if light is None: light = Item()
        if special is None: special = Item()
        if pet is None: pet = Item()
        
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
