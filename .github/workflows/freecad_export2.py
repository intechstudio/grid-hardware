import FreeCAD
import FreeCADGui
import TechDrawGui

import Part
import PartGui
import PartDesignGui

import sys

print(f"sys.argv = {sys.argv}")

import os 
if os.path.isdir("temp"):
  print("Directory already exists")
else:
  os.mkdir("temp")

objs = App.ActiveDocument.Objects
for obj in objs:
  sono=App.ActiveDocument.getObject(obj.Name)
  sono.ViewObject.show()

  if sono.TypeId == "App::Part":
    print(obj.Label, obj.Name, "STEP")
    if hasattr(sono, 'Shape'):
      sono.Shape.exportStep("temp/"+obj.Label+".step")
      __objs__=[]
      __objs__.append(App.ActiveDocument.getObject(obj.Name))
      print(__objs__)
      import ImportGui
      ImportGui.export(__objs__,"temp/"+obj.Label+"_test.step")
    else:
      print(".Shape not available")
      __objs__=[]
      __objs__.append(App.ActiveDocument.getObject(obj.Name))
      Part.export(__objs__,"temp/"+obj.Label+".step")