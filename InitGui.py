#***************************************************************************
#*                                                                         *
#*   copyright (c) 2015 - victor titov (deepsoic)                          *
#*                                               <vv.titov@gmail.com>      *
#*                                                                         *
#*   this program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the gnu lesser general public license (lgpl)    *
#*   as published by the free software foundation; either version 2 of     *
#*   the license, or (at your option) any later version.                   *
#*   for detail see the licence text file.                                 *
#*                                                                         *
#*   this program is distributed in the hope that it will be useful,       *
#*   but without any warranty; without even the implied warranty of        *
#*   merchantability or fitness for a particular purpose.  see the         *
#*   gnu library general public license for more details.                  *
#*                                                                         *
#*   you should have received a copy of the gnu library general public     *
#*   license along with this program; if not, write to the free software   *
#*   foundation, inc., 59 temple place, suite 330, boston, ma  02111-1307  *
#*   usa                                                                   *
#*                                                                         *
#***************************************************************************

__Comment__ = 'Advanced array tools and parametric compounding tools'
__Web__ = 'http://forum.freecadweb.org/viewtopic.php?f=22&t=12464'
__Wiki__ = ''
__Icon__  = ''
__Help__ = 'Install as a workbench - copy everything to path/to/FreeCAD/Mod/Lattice2'
__Author__ = 'DeepSOIC'
__Version__ = '2'
__Status__ = 'alpha'
__Requires__ = 'freecad 0.16.5155'
__Communication__ = 'vv.titov@gmail.com; DeepSOIC on FreeCAD forum'



class Lattice2Workbench (Workbench):
    MenuText = 'Lattice2'
    def __init__(self):
        # Hack: obtain path to Lattice by loading a dummy Py module
        import os
        import lattice2Dummy
        self.__class__.Icon = os.path.dirname(lattice2Dummy.__file__) + u"/PyResources/icons/Lattice2.svg".replace("/", os.path.sep)

    def Initialize(self):
        
        import Lattice2
        cmdsArrayTools = ([]
            + Lattice2.ArrayFeatures.Placement.exportedCommands
            + Lattice2.ArrayFeatures.LinearArray.exportedCommands
            + Lattice2.ArrayFeatures.PolarArray.exportedCommands
            + Lattice2.ArrayFeatures.ArrayFromShape.exportedCommands
            + Lattice2.ArrayFeatures.Invert.exportedCommands
            + Lattice2.ArrayFeatures.JoinArrays.exportedCommands
            + Lattice2.ArrayFeatures.ArrayFilter.exportedCommands
            + Lattice2.ArrayFeatures.ProjectArray.exportedCommands
            + Lattice2.ArrayFeatures.PopulateCopies.exportedCommands
            + Lattice2.ArrayFeatures.PopulateChildren.exportedCommands
            + Lattice2.ArrayFeatures.Resample.exportedCommands
            + Lattice2.ArrayFeatures.PopulateCopies.exportedCommands
        )
        self.appendToolbar('Lattice2ArrayFeatres', cmdsArrayTools)
        self.appendMenu('Lattice2', cmdsArrayTools)
        
        cmdsCompoundTools = ([]
            + Lattice2.CompoundFeatures.Downgrade.exportedCommands
            + Lattice2.CompoundFeatures.CompoundFilter.exportedCommands
            + Lattice2.CompoundFeatures.FuseCompound.exportedCommands        
            + Lattice2.CompoundFeatures.BoundBox.exportedCommands
            + Lattice2.CompoundFeatures.ShapeString.exportedCommands
        )
        self.appendToolbar('Lattice2CompoundFeatures', cmdsCompoundTools)
        self.appendMenu('Lattice2', cmdsCompoundTools)
        
        cmdsGuiTools = ([]
            + Lattice2.GuiTools.Inspect.exportedCommands
            + Lattice2.GuiTools.SubstituteObject.exportedCommands
        )
        self.appendToolbar('Lattice2GuiTools', cmdsGuiTools)
        self.appendMenu('Lattice2', cmdsGuiTools)

        
        cmdsRecomputeLocker = ([]
            + Lattice2.GuiTools.RecomputeLocker.exportedCommands
        )
        self.appendToolbar('Lattice2RecomputeLocker', cmdsRecomputeLocker)
        self.appendMenu('Recomputes', cmdsRecomputeLocker)

    def Activated(self):
        pass



Gui.addWorkbench(Lattice2Workbench())

