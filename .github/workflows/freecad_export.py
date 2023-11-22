import FreeCAD
import FreeCADGui
import TechDrawGui
import time



def export(tdg):
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


        tdg.export([sono], u"temp/"+obj.Label+".pdf")


from threading import Timer

def twoArgs(tdg, foo):
    export(tdg)
    print("tdg")
    print("")

def nArgs(*args):
    for each in args:
        print(each)

#arguments: 
#how long to wait (in seconds), 
#what function to call, 
#what gets passed in



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



r = Timer(6.0, twoArgs, (TechDrawGui, 123))
s = Timer(10.0, nArgs, ("OWLS","OWLS","OWLS"))

r.start()
s.start()

# time.sleep(5.0)

print("DONE")
#App.Gui.getMainWindow().close()

# sys.exit(0)
# exit(0)