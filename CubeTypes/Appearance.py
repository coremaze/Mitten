import struct
import io
from CubeTypes import FloatVector3

class Appearance():
    size = 172
    def __init__(self,
                 notUsed1 = 0,
                 notUsed2 = 0,
                 hairRed = 0,
                 hairGreen = 0,
                 hairBlue = 0,
                 notUsed3 = 0,
                 flags = 0,
                 scale = None,
                 headModel = 0,
                 hairModel = 0,
                 handModel = 0,
                 footModel = 0,
                 bodyModel = 0,
                 tailModel = 0,
                 shoulder2Model = 0,
                 wingModel = 0,
                 headScale = 1.0,
                 bodyScale = 1.0,
                 handScale = 1.0,
                 footScale = 1.0,
                 shoulder2Scale = 1.0,
                 weaponScale = 1.0,
                 tailScale = 1.0,
                 shoulderScale = 1.0,
                 wingScale = 1.0,
                 bodyRotation = 0.0,
                 armPitch = 0.0,
                 armRoll = 0.0,
                 armYaw = 0.0,
                 feetPitch = 0.0,
                 wingPitch = 0.0,
                 backPitch = 0.0,
                 bodyOffset = None,
                 headOffset = None,
                 handOffset = None,
                 footOffset = None,
                 tailOffset = None,
                 wingOffset = None):

        if scale is None: scale = FloatVector3(1.0, 1.0, 1.0)
        if bodyOffset is None: bodyOffset = FloatVector3()
        if headOffset is None: headOffset = FloatVector3()
        if handOffset is None: handOffset = FloatVector3()
        if footOffset is None: footOffset = FloatVector3()
        if tailOffset is None: tailOffset = FloatVector3()
        if wingOffset is None: wingOffset = FloatVector3()

        
        self.notUsed1 = notUsed1
        self.notUsed2 = notUsed2
        self.hairRed = hairRed
        self.hairGreen = hairGreen
        self.hairBlue = hairBlue
        self.notUsed3 = notUsed3
        self.flags = flags
        self.scale = scale
        self.headModel = headModel
        self.hairModel = hairModel
        self.handModel = handModel
        self.footModel = footModel
        self.bodyModel = bodyModel
        self.tailModel = tailModel
        self.shoulder2Model = shoulder2Model
        self.wingModel = wingModel
        self.headScale = headScale
        self.bodyScale = bodyScale
        self.handScale = handScale
        self.footScale = footScale
        self.shoulder2Scale = shoulder2Scale
        self.weaponScale = weaponScale
        self.tailScale = tailScale
        self.shoulderScale = shoulderScale
        self.wingScale = wingScale
        self.bodyRotation = bodyRotation
        self.armPitch = armPitch
        self.armRoll = armRoll
        self.armYaw = armYaw
        self.feetPitch = feetPitch
        self.wingPitch = wingPitch
        self.backPitch = backPitch
        self.bodyOffset = bodyOffset
        self.headOffset = headOffset
        self.handOffset = handOffset
        self.footOffset = footOffset
        self.tailOffset = tailOffset
        self.wingOffset = wingOffset

    @staticmethod
    def Import(data):
        notUsed1, = struct.unpack('<B', data.read(1))
        notUsed2, = struct.unpack('<B', data.read(1))
        hairRed, = struct.unpack('<B', data.read(1))
        hairGreen, = struct.unpack('<B', data.read(1))
        hairBlue, = struct.unpack('<B', data.read(1))
        notUsed3, = struct.unpack('<B', data.read(1))
        flags, = struct.unpack('<H', data.read(2))
        scale = FloatVector3.Import(data)
        headModel, = struct.unpack('<H', data.read(2))
        hairModel, = struct.unpack('<H', data.read(2))
        handModel, = struct.unpack('<H', data.read(2))
        footModel, = struct.unpack('<H', data.read(2))
        bodyModel, = struct.unpack('<H', data.read(2))
        tailModel, = struct.unpack('<H', data.read(2))
        shoulder2Model, = struct.unpack('<H', data.read(2))
        wingModel, = struct.unpack('<H', data.read(2))
        headScale, = struct.unpack('<f', data.read(4))
        bodyScale, = struct.unpack('<f', data.read(4))
        handScale, = struct.unpack('<f', data.read(4))
        footScale, = struct.unpack('<f', data.read(4))
        shoulder2Scale, = struct.unpack('<f', data.read(4))
        weaponScale, = struct.unpack('<f', data.read(4))
        tailScale, = struct.unpack('<f', data.read(4))
        shoulderScale, = struct.unpack('<f', data.read(4))
        wingScale, = struct.unpack('<f', data.read(4))
        bodyRotation, = struct.unpack('<f', data.read(4))
        armPitch, = struct.unpack('<f', data.read(4))
        armRoll, = struct.unpack('<f', data.read(4))
        armYaw, = struct.unpack('<f', data.read(4))
        feetPitch, = struct.unpack('<f', data.read(4))
        wingPitch, = struct.unpack('<f', data.read(4))
        backPitch, = struct.unpack('<f', data.read(4))
        bodyOffset = FloatVector3.Import(data)
        headOffset = FloatVector3.Import(data)
        handOffset = FloatVector3.Import(data)
        footOffset = FloatVector3.Import(data)
        tailOffset = FloatVector3.Import(data)
        wingOffset = FloatVector3.Import(data)
        
        return Appearance(notUsed1, notUsed2, hairRed, hairGreen, hairBlue, notUsed3,
                          flags, scale, headModel, hairModel, handModel, footModel,
                          bodyModel, tailModel, shoulder2Model, wingModel, headScale,
                          bodyScale, handScale, footScale, shoulder2Scale, weaponScale,
                          tailScale, shoulderScale, wingScale, bodyRotation, armPitch,
                          armRoll, armYaw, feetPitch, wingPitch, backPitch, bodyOffset,
                          headOffset, handOffset, footOffset, tailOffset, wingOffset)
    
    def Export(self):
        dataList = []
        dataList.append( struct.pack('<B', self.notUsed1) )
        dataList.append( struct.pack('<B', self.notUsed2) )
        dataList.append( struct.pack('<B', self.hairRed) )
        dataList.append( struct.pack('<B', self.hairGreen) )
        dataList.append( struct.pack('<B', self.hairBlue) )
        dataList.append( struct.pack('<B', self.notUsed3) )
        dataList.append( struct.pack('<H', self.flags) )
        dataList.append( self.scale.Export() )
        dataList.append( struct.pack('<H', self.headModel) )
        dataList.append( struct.pack('<H', self.hairModel) )
        dataList.append( struct.pack('<H', self.handModel) )
        dataList.append( struct.pack('<H', self.footModel) )
        dataList.append( struct.pack('<H', self.bodyModel) )
        dataList.append( struct.pack('<H', self.tailModel) )
        dataList.append( struct.pack('<H', self.shoulder2Model) )
        dataList.append( struct.pack('<H', self.wingModel) )
        dataList.append( struct.pack('<f', self.headScale) )
        dataList.append( struct.pack('<f', self.bodyScale) )
        dataList.append( struct.pack('<f', self.handScale) )
        dataList.append( struct.pack('<f', self.footScale) )
        dataList.append( struct.pack('<f', self.shoulder2Scale) )
        dataList.append( struct.pack('<f', self.weaponScale) )
        dataList.append( struct.pack('<f', self.tailScale) )
        dataList.append( struct.pack('<f', self.shoulderScale) )
        dataList.append( struct.pack('<f', self.wingScale) )
        dataList.append( struct.pack('<f', self.bodyRotation) )
        dataList.append( struct.pack('<f', self.armPitch) )
        dataList.append( struct.pack('<f', self.armRoll) )
        dataList.append( struct.pack('<f', self.armYaw) )
        dataList.append( struct.pack('<f', self.feetPitch) )
        dataList.append( struct.pack('<f', self.wingPitch) )
        dataList.append( struct.pack('<f', self.backPitch) )
        dataList.append( self.bodyOffset.Export() )
        dataList.append( self.headOffset.Export() )
        dataList.append( self.handOffset.Export() )
        dataList.append( self.footOffset.Export() )
        dataList.append( self.tailOffset.Export() )
        dataList.append( self.wingOffset.Export() )
        return b''.join(dataList)
        
