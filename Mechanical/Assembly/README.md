
## Used addons for assembly

[A2plus Workbench](https://wiki.freecad.org/A2plus_Workbench)

---

## Installing

It can easily be installed via the FreeCAD Addon Manager from the Tools/Addon Manager menu.

---

## Getting Started

To create an assembly create a new file in FreeCAD. At first this file needs to be saved. It is recommended (but not necessary) to save it in the same folder of the parts you want to assemble.

Now external parts can be added to the assembly by using the toolbar with the "Part icons with a plus sing". The button adds all bodies in the selected file as a single part. When using the button you can choose what part from a file should be imported as part. This way one can for example only import a sketch to assemble further parts using the sketch to determine the part positions.

The first added part gets a fixed position by default. (You can change this later via the part property)

Parts that are already in the assembly can be cloned with the "2 Part icon" button .

To edit a part from the assembly, select it in the model tree and use the "Part icon with a pencil" button . This will open the part into a new tab in FreeCAD or switch to its tab if the file is already opened.

To update changed parts in assemblies click on the "Part with a recycle sign" button. If you select one or some parts in FreeCAD's the tree view, A2plus will ask you to only update the selected parts.

Imported parts will keep their external dependencies and can be edited. For well-defined parts like screws it is however useful that their shape cannot be edited. This can be achieved with the "Yellow and red part icons" button that converts the selected part to a static copy of the original part.

Toggling the "Mouse" button sets the way you can select several several edges, faces etc.: Either with a single click or by Ctrl+click. 

---

## Assembling

Assembling parts is done by adding constraints between parts. After a constraint A2plus will move the parts according to the constraint if possible.

To create a constraint between parts, keep the Ctrl key pressed and select each an edge or face of two parts. Then click the toolbar button of the desired constraint. A dialog will pop up that is descried in section Constraints. The constraint will be added in the model tree attached to the affected parts.

For complex constraints between parts A2plus might fail to solve the constraints. Therefore also have a look at section Troubleshooting for strategies to resolve such cases. 

You can get to know each constrain [here](https://wiki.freecad.org/A2plus_Workbench).