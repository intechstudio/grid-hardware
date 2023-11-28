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

def hideAll():
  doc = App.ActiveDocument
  assert(doc)
  bodies = [obj for obj in doc.Objects if obj.isDerivedFrom("PartDesign::Body")]
  shown = []
  for body in bodies:
    grp = body.Group
    # print (body.Label)
    App.Gui.ActiveDocument.getObject(body.Name).hide()

def showPartDesignBody(name):
  doc = App.ActiveDocument
  assert(doc)
  bodies = [obj for obj in doc.Objects if obj.isDerivedFrom("PartDesign::Body")]
  shown = []
  hideAll()
  for body in bodies:
    if body.Label == name:
      grp = body.Group
      #print (body.Label)
      App.Gui.ActiveDocument.getObject(body.Name).show()
      for feat in body.Origin.OriginFeatures:
        if feat.Label in shown:
          continue
        shown.append(feat.Label)

      for item in grp:
        if item.TypeId == "Sketcher::SketchObject":
          continue

        #print(f"-->{item.TypeId} {item.Label}")
        App.Gui.ActiveDocument.getObject(item.Name).show()

def exportScreenshot(label, filename):
  hideAll()
  showPartDesignBody(label)

  view = App.Gui.ActiveDocument.ActiveView
  print("STEP 1",filename, dir(view), vars(view))
  FreeCADGui.updateGui()
  print("STEP 2",filename)
  #view.viewAxometric()
  print("STEP 3",filename)
  #view.fitAll()
  print("STEP 4",filename)
  FreeCADGui.updateGui()
  print("STEP 5",filename)
  
  print("SCREENSHOT", label, filename)
  App.Gui.ActiveDocument.ActiveView.saveImage(filename,3200,2400,'Transparent')

  hideAll()

# Ez kell ide
FreeCADGui.updateGui()
FreeCADGui.updateGui()
FreeCADGui.updateGui()
FreeCADGui.updateGui()
FreeCADGui.updateGui()
FreeCADGui.updateGui()

hideAll()

objs = App.ActiveDocument.Objects
for obj in objs:
  sono=App.ActiveDocument.getObject(obj.Name)

for obj in objs:
  sono=App.ActiveDocument.getObject(obj.Name)
  sono.ViewObject.show()
  if sono.TypeId == "PartDesign::Body":

    if "png" in export_list:
      print(obj.Label, obj.Name, "PNG")
      exportScreenshot(obj.Label, "temp/"+obj.Label+".png")

    if "step" in export_list:
      print(obj.Label, obj.Name, "STEP")

      sono.Shape.exportStep("temp/"+obj.Label+".step")

    if "stl" in export_list:
      print(obj.Label, obj.Name, "STL")
      sono.Shape.exportStl("temp/"+obj.Label+".stl")

  elif sono.TypeId == "TechDraw::DrawPage":

    if "pdf" in export_list:
      print(obj.Label, obj.Name, "DRAW")
      TechDrawGui.export([sono],u"temp/"+obj.Label+".pdf")
  sono.ViewObject.hide()


hideAll()




print("DONE")

App.Gui.SendMsgToActiveView("Save")
print("DONE2")

App.ActiveDocument.save()
print("DONE3")


App.Gui.getMainWindow().close()

# sys.exit(0)
# exit(0)