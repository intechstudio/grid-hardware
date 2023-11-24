import FreeCAD
import FreeCADGui
import TechDrawGui

import sys

print(f"sys.argv = {sys.argv}")

import os 
if os.path.isdir("temp"):
  print("Directory already exists")
else:
  os.mkdir("temp")

export_list = sys.argv[3:]

print(f"export_list = {export_list}")

if "stl" in export_list:
  print("export stl requested")
if "step" in export_list:
  print("export step requested")
if "pdf" in export_list:
  print("export pdf requested")


docname = sys.argv[2]
print("Opening document: ", docname, os.path.isfile(docname))
App.openDocument(docname)


FreeCADGui.updateGui()

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

App.Gui.SendMsgToActiveView("Save")
print("DONE2")

App.ActiveDocument.save()
print("DONE3")


App.Gui.getMainWindow().close()

# sys.exit(0)
# exit(0)