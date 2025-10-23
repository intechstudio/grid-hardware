import cadquery as cq
up_thickness = 1
down_thickness = 1
corner_fillet = 0.35
pattern_spacing = 26.67

plate_size = 104.3

bolt_dia = 1.6 + 0.2
bolt_spacing = 100

mag_x = 47*2
mag_y = 51.7*2

# Define the 2D profile points for the magnet covering stud relative to the magnet position
stud_base_width=3
stud_top_width=1.8
stud_height=1.05

points = [
    (stud_base_width/2, 0),
    (stud_top_width/2, stud_height),
    (-stud_top_width/2, stud_height),
    (-stud_base_width/2, 0)
]

# Build the solid
stud = (
    cq.Workplane("XY")
    .center(mag_x/2, mag_y/2)
    .polyline(points)
    .close()
    .extrude(up_thickness)
)

# Union it with the mirror of itself
stud = stud.union(stud.mirror("YZ"))

# Apply a polar patter
for angle in (90, 180, 270):
    stud = stud.union(stud.rotate((0, 0, 0), (0, 0, 1), angle))
    
    
# base plate
r = cq.Workplane("XY").rect(plate_size, plate_size).extrude(up_thickness)\
    .faces("<Z").extrude(-down_thickness).workplane().rarray(bolt_spacing, bolt_spacing, 2, 2).hole(bolt_dia)\
    .edges("|Z").fillet(corner_fillet)

# ===================== DOWN THICKNESS ======================== #

spacer_dia = 7 + 0.5
lip_pos = 51.37 - 1 # Must subtract the thickness of the INTERFACE board
mag_dia = 5.5
mag_fillet = 0.72 #measured from model
lip_tolerance=0.25

r = r.faces(">Z").workplane(offset=-up_thickness)\
    .rarray(pattern_spacing*2, pattern_spacing*2, 2, 2).circle(spacer_dia/2).cutBlind(-10)\
    .rarray(mag_x, mag_y, 2, 2).circle(mag_dia/2+lip_tolerance).cutBlind(-10)\
    .rarray(mag_y, mag_x, 2, 2).circle(mag_dia/2+lip_tolerance).cutBlind(-10)\
    .rarray(102, 102, 2, 2).circle(3.5).cutBlind(-10)\
    .polarArray(lip_pos+2-lip_tolerance,0,360,4).rect(4,95).cutBlind(-10)\
    .edges("|Z").fillet(mag_fillet-lip_tolerance/2)

r = r.union(stud)

# ===================== USER INTERFACE ======================== #

pot_dia = 8
led_dia = 2.9
led_offset = 8.5

r = r.faces(">Z").workplane()\
    .rarray(pattern_spacing, pattern_spacing, 4, 4).hole(pot_dia)\
    .center(0,led_offset).rarray(pattern_spacing, pattern_spacing, 4, 4).hole(led_dia)\
    .faces(">Z").workplane(offset=-up_thickness).center(0,led_dia/2 + 3*pattern_spacing/2).rarray(pattern_spacing, pattern_spacing, 4, 1).rect(led_dia*0.6, led_dia*0.6).cutBlind(-10)

# ====================== LIGHTPIPE =========================== #

# 0.2 is the support breakaway tolerance
support_tolerance=(0.2)
led_distance = 7.35 - support_tolerance
board_distance = 8.5 - support_tolerance
led_y = 47.625
ledpipe_y = 40.005+8.5
led_diameter = 2.85

#.faces(">Z").workplane(offset=-up_thickness-down_thickness)

# LED Y POSITION ON FADER MODULE FP(PCB): PBF4: 25 (25.4k)  EF44: 29.5 (29.46)
    
led_body = (
    cq.Workplane("XY").workplane(offset=up_thickness).center(0, ledpipe_y)
    .circle(led_diameter/2).extrude(-up_thickness-down_thickness)\
    .faces(">Z").workplane(offset=-up_thickness-down_thickness).circle(3/2)\
    .workplane(offset=down_thickness-led_distance).center(0,led_y-ledpipe_y).rect(2.0,2.0).center(0,-led_y+ledpipe_y)\
    .loft()\
    .faces(">Z").workplane(offset=-up_thickness-down_thickness).rect(11.5,1.5).extrude(+down_thickness-led_distance+2.5)\
    .faces(">Z").workplane(offset=-up_thickness-down_thickness).center(5,led_y-ledpipe_y).rect(1.5,2).center(-10,0).rect(1.5,2).center(5,-led_y+ledpipe_y).extrude(+down_thickness-board_distance)\
    .faces(">Z").workplane(offset=-up_thickness-down_thickness).center(5,0).circle(1.5/2).center(-10,0).circle(1.5/2).center(5,0).extrude(down_thickness)\
    .faces("<Y").workplane().center(-2,-down_thickness-1+support_tolerance/2).rect(1,2.5)\
    .center(4,0).rect(1,2.5).cutBlind(-10)
)

    
pressfit_dia = 3   
pressfit_width = 0.25 
pressfit_chamfer = pressfit_width / 2.5
led_fitting = cq.Workplane("XY").workplane(offset=up_thickness).center(0, ledpipe_y).workplane().rect(pressfit_dia,pressfit_width).extrude(-up_thickness-down_thickness)
led_fitting = led_fitting.faces(">Z").workplane().rect(pressfit_width,pressfit_dia).extrude(-up_thickness-down_thickness)
led_fitting = led_fitting.faces(">Z").edges().chamfer(pressfit_chamfer)
    
led_body = led_body.union(led_fitting)

slot_inner_dia = 7.5
slot_inner_len = 12.5
slot_inner_offset = (slot_inner_len-slot_inner_dia)/2
slot_outter_dia = 7.5+1.5*2
slot_outter_len = 15
slot_outter_offset = (slot_outter_len-slot_outter_dia)/2
bump_position =  (slot_outter_offset/2 + slot_outter_len/2 + slot_inner_offset/2 + slot_inner_len/2)/2
bump_dia = (slot_outter_dia- slot_inner_dia)/2


led_bridge = (
    cq.Workplane("XY").workplane(offset=-down_thickness).center(0, ledpipe_y).rect(70,1.5).extrude(-2)\
    .faces(">Z").workplane().center(0,-29.46+26.67).center(0,slot_outter_offset).rarray(26.67*2,0,2,1).slot2D(slot_outter_len,slot_outter_dia, angle=90).center(0,-slot_outter_offset).extrude(-2)\
    .faces(">Z").workplane().center(0,slot_inner_offset).rarray(26.67*2,0,2,1).slot2D(slot_inner_len,slot_inner_dia, angle=90).center(0,-slot_inner_offset).cutBlind(-2)\
    .faces(">Z").workplane().center(0, +29.46-26.67 + 15).rarray(26.67*2,0,2,1).rect(50,30-1.5).cutBlind(-2)\
    .faces(">Y").workplane().rarray(26.67,0,2,1).rect(10,10).cutBlind(-10)
    
)
    
led_bridge = led_bridge.faces(">Z").workplane().center(0,-bump_position).rarray(26.67*2,0,2,1).circle(bump_dia/2).extrude(down_thickness)
# start with your single piece

# make an array of 4 parts, 26.67 mm apart in X
parts = [led_body.translate((i * 26.67-40.005, 0, 0)) for i in range(4)]

# fuse them all together
result = parts[0]
for p in parts[1:]:
    result = result.union(p)

result = result.union(led_bridge)
results = [result.translate((0, i * 7, 0)) for i in range(4)]
unioned = results[0]
for r in results[1:]:
    unioned = unioned.union(r)

# show_object(led_bridge)
# show_object(led_body)
show_object(unioned)
