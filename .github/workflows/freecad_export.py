import FreeCAD
import FreeCADGui
import TechDrawGui

import sys

print(f"sys.argv = {sys.argv}")

export_list = sys.argv[3:]

print(f"export_list = {export_list}")

if "stl" in export_list:
  print("export stl requested")
if "step" in export_list:
  print("export step requested")
if "pdf" in export_list:
  print("export pdf requested")

App.openDocument(sys.argv[1]+".FCStd")
objs = App.ActiveDocument.Objects
for obj in objs:
  sono=App.ActiveDocument.getObject(obj.Name)
  if sono.TypeId == "PartDesign::Body":

    if "stl" in export_list:
      print(obj.Label, "STEP")
      sono.Shape.exportStep("temp/"+obj.Label+".step")

    if "stl" in export_list:
      print(obj.Label, "STL")
      sono.Shape.exportStl("temp/"+obj.Label+".stl")

  elif sono.TypeId == "TechDraw::DrawPage":

    if "pdf" in export_list:
      print(obj.Label, "DRAW")
      TechDrawGui.export([sono],u"temp/"+obj.Label+".pdf")


print("DONE")

Gui.SendMsgToActiveView("Save")
App.ActiveDocument.save()
App.Gui.getMainWindow().close()

# exit(0)