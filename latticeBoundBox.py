from latticeCommon import *


__title__="BoundingBox module for FreeCAD"
__author__ = "DeepSOIC"
__url__ = ""



# -------------------------- common stuff --------------------------------------------------

def boundBox2RealBox(bb):
    base = FreeCAD.Vector(bb.XMin, bb.YMin, bb.ZMin)
    OX = FreeCAD.Vector(1, 0, 0)
    OY = FreeCAD.Vector(0, 1, 0)
    OZ = FreeCAD.Vector(0, 0, 1)
    if bb.XLength > DistConfusion and bb.YLength > DistConfusion and bb.ZLength > DistConfusion :
        return Part.makeBox(bb.XLength,bb.YLength,bb.ZLength, base, OZ)
    elif bb.XLength > DistConfusion and bb.YLength > DistConfusion:
        return Part.makePlane(bb.XLength, bb.YLength, base, OZ, OX)
    elif bb.XLength > DistConfusion and bb.ZLength > DistConfusion :
        return Part.makePlane(bb.XLength, bb.ZLength, base, OY*-1, OX)
    elif bb.YLength > DistConfusion and bb.ZLength > DistConfusion :
        return Part.makePlane(bb.YLength, bb.ZLength, base, OX, OY)
    elif bb.XLength > DistConfusion:
        return Part.makeLine(base, base + OX*bb.XLength)
    elif bb.YLength > DistConfusion:
        return Part.makeLine(base, base + OY*bb.YLength)
    elif bb.ZLength > DistConfusion:
        return Part.makeLine(base, base + OZ*bb.ZLength)
    else:
        raise ValueError("Bounding box is zero")
        
def scaledBoundBox(bb, scale):
    bb2 = FreeCAD.BoundBox(bb)
    cnt = bb.Center
    bb2.XMin = (bb.XMin - cnt.x)*scale + cnt.x
    bb2.YMin = (bb.YMin - cnt.y)*scale + cnt.y
    bb2.ZMin = (bb.ZMin - cnt.z)*scale + cnt.z
    bb2.XMax = (bb.XMax - cnt.x)*scale + cnt.x
    bb2.YMax = (bb.YMax - cnt.y)*scale + cnt.y
    bb2.ZMax = (bb.ZMax - cnt.z)*scale + cnt.z
    return bb2
    
def getPrecisionBoundBox(shape):
    # First, we need a box that for sure contains the object.
    # We use imprecise bound box, scaled up twice. The scaling
    # is required, because the imprecise bound box is often a
    # bit smaller than the shape.
    bb = scaledBoundBox(shape.BoundBox, 2.0)
    # Make sure bound box is not collapsed in any direction, 
    # to make sure boundBox2RealBox returns a box, not plane
    # or line
    if bb.XLength < DistConfusion or bb.YLength < DistConfusion or bb.ZLength < DistConfusion:
        bb.enlarge(1.0)
    
    # Make a boundingbox shape and compute distances from faces
    # of this enlarged bounding box to the actual shape. Shrink
    # the boundbox by the distances.
    bbshape = boundBox2RealBox(bb)
    #FIXME: it may be a good idea to not use hard-coded face indexes
    bb.XMin = bb.XMin + shape.distToShape(bbshape.Faces[0])[0]
    bb.YMin = bb.YMin + shape.distToShape(bbshape.Faces[2])[0]
    bb.ZMin = bb.ZMin + shape.distToShape(bbshape.Faces[4])[0]
    bb.XMax = bb.XMax - shape.distToShape(bbshape.Faces[1])[0]
    bb.YMax = bb.YMax - shape.distToShape(bbshape.Faces[3])[0]
    bb.ZMax = bb.ZMax - shape.distToShape(bbshape.Faces[5])[0]
    return bb


def makeBoundBox(name):
    '''makeBoundBox(name): makes a BoundBox object.'''
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
    _BoundBox(obj)
    _ViewProviderBoundBox(obj.ViewObject)
    return obj

class _BoundBox:
    "The BoundBox object"
    def __init__(self,obj):
        self.Type = "BoundBox"
        obj.addProperty("App::PropertyLink","Base","BoundBox","Object to make boundingbox")
        obj.addProperty("App::PropertyBool","Precision","BoundBox","Use precise alorithm (slower).")
        obj.Precision = True
        obj.addProperty("App::PropertyBool","InLocalSpace","BoundBox","Construct bounding box in local coordinate space of the object, not in global.")
        obj.Proxy = self
        

    def execute(self,obj):
        shape = obj.Base.Shape
        
        if obj.InLocalSpace:
            shape = shape.copy()
            shape.transformShape(obj.Base.Placement.inverse().toMatrix())
        
        rst = boundBox2RealBox(getPrecisionBoundBox(shape))
        
        if obj.InLocalSpace:
            rst.transformShape(obj.Base.Placement.toMatrix(), True) #True is for Copy argument
        
        obj.Shape = rst
        return
        
        
class _ViewProviderBoundBox:
    "A View Provider for the BoundBox object"

    def __init__(self,vobj):
        vobj.Proxy = self
        vobj.DisplayMode = "Wireframe"
       
    def getIcon(self):
        return getIconPath("Lattice_BoundBox.svg")

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object

  
    def setEdit(self,vobj,mode):
        return False
    
    def unsetEdit(self,vobj,mode):
        return

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None

def CreateBoundBox(name):
    FreeCAD.ActiveDocument.openTransaction("Create BoundBox")
    FreeCADGui.addModule("latticeBoundBox")
    FreeCADGui.doCommand("f = latticeBoundBox.makeBoundBox(name='"+name+"')")
    FreeCADGui.doCommand("f.Base = FreeCADGui.Selection.getSelection()[0]")
    FreeCADGui.doCommand("f.Proxy.execute(f)")
    FreeCADGui.doCommand("f.purgeTouched()")
    FreeCADGui.doCommand("f = None")
    FreeCAD.ActiveDocument.commitTransaction()


# -------------------------- /common stuff --------------------------------------------------

# -------------------------- Gui command --------------------------------------------------

class _CommandBoundBox:
    "Command to create BoundBox feature"
    def GetResources(self):
        return {'Pixmap'  : getIconPath("Lattice_BoundBox.svg"),
                'MenuText': QtCore.QT_TRANSLATE_NOOP("Lattice_BoundBox","Parametric bounding box"),
                'Accel': "",
                'ToolTip': QtCore.QT_TRANSLATE_NOOP("Lattice_BoundBox","Make a box that precisely fits the object")}
        
    def Activated(self):
        if len(FreeCADGui.Selection.getSelection()) == 1 :
            CreateBoundBox(name = "BoundBox")
        else:
            mb = QtGui.QMessageBox()
            mb.setIcon(mb.Icon.Warning)
            mb.setText(_translate("Lattice_BoundBox", "Select a shape to make a bounding box for, first!", None))
            mb.setWindowTitle(_translate("Lattice_BoundBox","Bad selection", None))
            mb.exec_()
            
    def IsActive(self):
        if FreeCAD.ActiveDocument:
            return True
        else:
            return False
            
FreeCADGui.addCommand('Lattice_BoundBox', _CommandBoundBox())

exportedCommands = ['Lattice_BoundBox']

# -------------------------- /Gui command --------------------------------------------------
