import cadquery as cq


grid_nominal = 106.68
grid_width = grid_nominal + 0.4
grid_height = 16
jig_height = grid_height+2
jig_wall = 4
mag_dia = 3
mag_dist = 94


result = cq.Workplane("XY" ).box(grid_width + 2*jig_wall, grid_width + 2*jig_wall, jig_height)
result = result.faces(">Z").rect(grid_width, grid_width).cutBlind(-grid_height)
result = result.faces(">Z").rect(90, 90).cutBlind(-grid_height*2)
result = result.faces(">Z").rect(grid_width+jig_wall, 85).cutBlind(-grid_height)
result = result.faces(">Z").rect(85, grid_width+jig_wall).cutBlind(-grid_height)
result = result.faces(">Z").workplane(offset=-1).rarray(grid_width+mag_dia-0.01,mag_dist,2,2).circle(mag_dia/2).cutBlind(-grid_height*2)
result = result.faces(">Z").workplane(offset=-1).rarray(mag_dist,grid_width+mag_dia-0.01,2,2).circle(mag_dia/2).cutBlind(-grid_height*2)
result = result.faces(">Z").rect(85, 200).cutBlind(-grid_height+6)
result = result.faces(">Z").rect(200, 85).cutBlind(-grid_height+6)
result = result.edges("<Z").chamfer(0.4)
result = result.edges(">Z").chamfer(0.8)
result = result.edges("|Z").chamfer(0.6)
show_object(result)