# What is Lattice2 workbench
Lattice Workbench is a plug-in module for FreeCAD.

The workbench purpose is working with placements and arrays of placements. It is a sort of assembly workbench, but with emphasis on arrays. There are no constraints and relations, there are just arrays of placements that can be generated, combined, transformed, superimposed and populated with shapes. 

Ever wondered how to create a protractor with FreeCAD? That's the aim of the workbench (including tick labeling). Also, exploded assemblies can be made with the workbench.

Additionally, the workbench features a few general-purpose tools, such as parametric downgrade, bounding boxes, shape info tool, and tools for working with compounds.

One of the big design goals of the workbench is being as parametric as possible.

# Why Lattice2, not just Lattice?
Lattice2 was created at the moment when breaking changes needed to be made, but there were a few things made with Lattice. So, it was decided to keep the workbench in that time's state indefinitely as version 1.0, and start development of a new version.

The goal was to be able to have both Lattice v1 and v2 in a single FreeCAD installation. So a new repository was started, and all the files were renamed to start with 'lattice2' or otherwise differ from those of Lattice v1.

# Highlights
Let's have a glance over the most important capabilities that the workbench adds to FreeCAD:

* Re-use arrays as many times as you need. Unlike Draft array, which directly generates the array of shapes, lattice array tools generate arrays of placements. These can later be populated with shapes, as many times as necessary, without having to set up another array.

* Elements of array can be different. Unlike Draft Arrays, which always generate a set of equal shapes, Lattice arrays can be used to arrange a set of different shapes. Pack the shapes to be arranged into a Compound, and use Lattice Compose feature to arrange them.

* Arrays of placements can be combined, inverted, generated from existing shape arrangements, made from individual placements, projected onto shapes, filtered, etc. This allows to produce complex arrangements without scripting.

* single placements can be used for primitive assembling of parts.

* linear arrays and polar arrays can have their axes linked to edges of shapes

* parametric explode commands allow extraction of specific elements of arrays, without losing parametric relation to the original. 

# Download/install
repository: https://github.com/DeepSOIC/Lattice2

Installation: download zip, unpack the contents into a "Lattice" folder created in \Path\to\FreeCAD\Mod, restart FreeCAD. Lattice workbench was also packaged to Launchpad in the Ubuntu FreeCAD Community PPA. 

Lattice WB requires FreeCAD no less than v0.16.5155 (only available as development snapshots at the moment of writing). In earlier FreeCADs, dropdown toolbar buttons are not going to work, making many useful commands unavailable (and possibly, total inability to load the workbench). That may be fixed at some point in future.

The workbench is OS independent, it should work on any system FreeCAD can be run on. If you find that it doesn't - that is a bug. Please make an issue.

# License
Lattice workbench is licenced under LGPL V2, just like FreeCAD. For more info, see copying.lib file in the repository.

# Status
This version is in devlopment. Breaking changes can be introduced at any point. If you want to make a project with use of Lattice workbench, it is recommended to stick with Lattice v1.

Lattice v1 is available here: https://github.com/DeepSOIC/Lattice
