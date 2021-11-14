# -*- coding: utf-8 -*-
import FreeCAD
App.openDocument("\Mechanical\Assembly\Frontpanel\grid_frontpanel.FCStd")
objs = App.ActiveDocument.RootObjects
for obj in objs:
	sono=App.ActiveDocument.getObject(obj.Name)
	print(obj.Label)
	sono.Shape.exportStep("/"+obj.Label+".step")
