#!/usr/bin/env python 
'''
Copyright (C) 2005,2007,2008 Aaron Spike, aaron@ekips.org
Copyright (C) 2008,2010 Alvin Penner, penner@vaxxine.com

This file output script for Inkscape creates a AutoCAD R14 DXF file.
The spec can be found here: http://www.autodesk.com/techpubs/autocad/acadr14/dxf/index.htm.

File history:
- template dxf_outlines.dxf added Feb 2008 by Alvin Penner
- ROBO-Master output option added Aug 2008
- ROBO-Master multispline output added Sept 2008
- LWPOLYLINE output modification added Dec 2008
- toggle between LINE/LWPOLYLINE added Jan 2010
- support for transform elements added July 2010
- support for layers added July 2010
- support for rectangle added Dec 2010

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
# standard library
import math
# local library
import inkex
import simplestyle
import simpletransform
import cubicsuperpath
import coloreffect
import dxf_templates
import cspsubdiv
import simplepath

inkex.localize()

try:
    from numpy import *
    from numpy.linalg import solve
except:
    inkex.errormsg(_("Failed to import the numpy or numpy.linalg modules. These modules are required by this extension. Please install them and try again."))
    inkex.sys.exit()

def pointdistance((x1,y1),(x2,y2)):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

def get_fit(u, csp, col):
    return (1-u)**3*csp[0][col] + 3*(1-u)**2*u*csp[1][col] + 3*(1-u)*u**2*csp[2][col] + u**3*csp[3][col]

def get_matrix(u, i, j):
    if j == i + 2:
        return (u[i]-u[i-1])*(u[i]-u[i-1])/(u[i+2]-u[i-1])/(u[i+1]-u[i-1])
    elif j == i + 1:
        return ((u[i]-u[i-1])*(u[i+2]-u[i])/(u[i+2]-u[i-1]) + (u[i+1]-u[i])*(u[i]-u[i-2])/(u[i+1]-u[i-2]))/(u[i+1]-u[i-1])
    elif j == i:
        return (u[i+1]-u[i])*(u[i+1]-u[i])/(u[i+1]-u[i-2])/(u[i+1]-u[i-1])
    else:
        return 0

def convert_arc_abrxry0_to_crxry00102(a, b, rx, ry, theta, largearc, sweep):
    # Convert from degrees
    theta_rads = radians(theta)

    # Create Transforms to transform our ellipse to a unit circle and back:
    T = matrix([[cos(theta_rads) / rx, sin(theta_rads) / rx],[-sin(theta_rads) / ry, cos(theta_rads) / ry]])
    T_inv = T.I

    # Create a position vector matrix of our two points
    ab_vecs = matrix([[a[0],b[0]],[a[1],b[1]]])

    # Transform to unit circle space:
    ab_dash_vecs = T * ab_vecs

    # Find the mid point:
    am_vec = (ab_dash_vecs[:,1] - ab_dash_vecs[:,0]) * 0.5
    am_x = am_vec[0,0]
    am_y = am_vec[1,0]

    # find the vector perpendicular to the line am.
    # Depending on the sweep parameter, our centre is either one side or the other of the mid point
    # and hence the perp is either positive or negative:
    if sweep and largearc or not (sweep or largearc):
        am_perp_vec = matrix([[am_y],[-am_x]])
    else:
        am_perp_vec = matrix([[-am_y],[am_x]])

    # find the (square of) the length of the line am:
    mag_am2 = am_x * am_x + am_y * am_y
    # Use pythagorus to find distance to the centre:
    tmp = 1.0 - mag_am2
    if tmp < -0.001:
        inkex.errormsg(_("Elipse conversion failed, Can't sqrt(%f). Possibly due to radii too small.") % (tmp))
        inkex.sys.exit()
    elif tmp < 0:
        mag_mc = 0
    else:
        mag_mc = sqrt(tmp)

    # Find the centre from point a, via the midpoint:
    c = ab_dash_vecs[:,0] + am_vec + (mag_mc / sqrt(mag_am2)) * am_perp_vec

    # Use inverse trig to find angles:

    theta1 = math.acos(ab_dash_vecs[0,0]-c[0,0])
    if ab_dash_vecs[1,0]-c[1,0] < 0.0:
        theta1 = math.pi * 2 - theta1
    theta2 = math.acos(ab_dash_vecs[0,1]-c[0,0])
    if ab_dash_vecs[1,1]-c[1,0] < 0.0:
        theta2 = math.pi * 2 - theta2

    # correct for start and end angles for sweep direction:
    if sweep:
        if theta1 > theta2:
            # the round is an ugly fudge because I was get some 'nearly but not quite'
            if round(theta1 / math.pi,5) >= 2.0 :
                theta1 = theta1 - 2*math.pi
            else:
                theta2 = theta2 + 2*math.pi
    else:
        if theta2 > theta1:
            if round(theta2 / math.pi,5) >= 2.0 :
                theta2  = theta2 - 2*math.pi
            else:
                theta1 = theta1 + 2*math.pi

    # convert back to ellipse space and convert to point:
    cpt = (T_inv * c).getA().ravel().tolist()

    return [ cpt, rx, ry, theta, theta1, theta2 ];

def split_arc_nonarc(simplep):
    nonarcpath = []
    arcpath = []
    pos = []
    start = []
    broken = False
    lastcmd = ''
    for s in simplep:
        cmd, params = s        
        if cmd == 'M':
            pos = params[:]
            start = pos[:]
            broken = False
        elif cmd == 'A':
            if lastcmd != 'A':
                arcpath.append(['M', pos ])
            arcpath.append(s[:])
            pos = params[-2:]
            broken = True
        else:
            if lastcmd == 'A' or lastcmd == 'M':
                nonarcpath.append(['M', pos ])
            if cmd == 'Z' or cmd == 'z':
                if broken:
                    if abs(pos[0]-start[0]) > 0.0001 or abs(pos[1]-start[1]) > 0.0001:
                        nonarcpath.append(['L', start])
                else:
                    nonarcpath.append(s)
                broken = False
                pos = start
            else:
                nonarcpath.append(s)
                pos = params[-2:]
        lastcmd = cmd

    return [nonarcpath,arcpath]    

class MyEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-R", "--ROBO", action="store",
                                     type="string", dest="ROBO",
                                     default=False)
        self.OptionParser.add_option("-P", "--POLY", action="store",
                                     type="string", dest="POLY",
                                     default=True)
        self.OptionParser.add_option("-F", "--FLATTENBES", action="store",
                                     type="string", dest="FLATTENBES",
                                     default=True)
        self.OptionParser.add_option("--units", action="store",
                                     type="string", dest="units",
                                     default="72./90") # Points
        self.OptionParser.add_option("--encoding", action="store",
                                     type="string", dest="char_encode",
                                     default="latin_1")
        self.OptionParser.add_option("--tab", action="store",
                                     type="string", dest="tab")
        self.OptionParser.add_option("--inputhelp", action="store",
                                     type="string", dest="inputhelp")
        self.OptionParser.add_option("--layer_option", action="store",
                                     type="string", dest="layer_option",
                                     default="all")
        self.OptionParser.add_option("--layer_name", action="store",
                                     type="string", dest="layer_name")
        self.OptionParser.add_option("-f", "--flatness",
                        action="store", type="float", 
                        dest="flat", default=0.1,
                        help="Minimum flatness of the subdivided curves")
                                     
        self.dxf = []
        self.handle = 255                       # handle for DXF ENTITY
        self.layers = ['0']
        self.layer = '0'                        # mandatory layer
        self.layernames = []
        self.csp_old = [[0.0,0.0]]*4            # previous spline
        self.d = array([0], float)              # knot vector
        self.poly = [[0.0,0.0]]                 # LWPOLYLINE data
    def output(self):
        print ''.join(self.dxf)
    def dxf_add(self, str):
        self.dxf.append(str.encode(self.options.char_encode))
    def dxf_line(self,csp):
        self.handle += 1
        self.dxf_add("  0\nLINE\n  5\n%x\n100\nAcDbEntity\n  8\n%s\n 62\n%d\n100\nAcDbLine\n" % (self.handle, self.layer, self.color))
        self.dxf_add(" 10\n%f\n 20\n%f\n 30\n0.0\n 11\n%f\n 21\n%f\n 31\n0.0\n" % (csp[0][0],csp[0][1],csp[1][0],csp[1][1]))
    def dxf_arc(self,cp,maxisp,rmm,a0,a1):
        self.handle += 1
        self.dxf_add("  0\nELLIPSE\n  5\n%x\n100\nAcDbEntity\n  8\n%s\n 62\n%d\n100\nAcDbEllipse\n" % (self.handle, self.layer, self.color))
        self.dxf_add(" 10\n%f\n 20\n%f\n 30\n0.0\n 11\n%f\n 21\n%f\n 31\n0.0\n 40\n%f\n 41\n%f\n 42\n%f\n" % (cp[0],cp[1],maxisp[0],maxisp[1],rmm,a0,a1))
    def dxf_arc_transform(self,m,cx,cy,rx,ry,abase,a0,a1):
        cp = [cx,cy]
        abaserads = math.radians(abase)
        if rx >= ry:
            abaserads = abaserads + math.pi
            rmaj = rx
            rmin = ry
            # major axis vector points left

            # angles in inkscape = cw from elipse local x axis;
            # angles in dxf ccw from major axis
            # major axis at Pi
            # so invert and offset by Pi
            a0 = math.pi - a0
            a1 = math.pi - a1
        else:
            abaserads = abaserads - math.pi / 2
            rmaj = ry
            rmin = rx
            # major axis vector is up the page (-ve y in inkscape)

            # angles in inkscape = cw from elipse local x axis;
            # angles in dxf ccw from major axis
            # major axis at 3 * Pi / 2
            # so invert and offset by 3 * Pi / 2
            a0 = 3 * math.pi / 2 - a0
            a1 = 3 * math.pi / 2 - a1
        rmm = rmin / rmaj
        majaxisp = [cx + rmaj*cos(abaserads), cy + rmaj*sin(abaserads)]

        if ((a0 < 0) or (a1 < 0)):
            a0 = a0 + 2 * math.pi
            a1 = a1 + 2 * math.pi
        
        # apply transforms
        simpletransform.applyTransformToPoint(m,cp)
        simpletransform.applyTransformToPoint(m,majaxisp)

        # Maj axis is relative to centre...
        majaxisp[0] = majaxisp[0] - cp[0]
        majaxisp[1] = majaxisp[1] - cp[1]

        # reverse angles from inkscape cw to DXF ccw
        self.dxf_arc(cp,majaxisp,rmm,a1,a0)
        
    def LWPOLY_line(self,csp):
        if (abs(csp[0][0] - self.poly[-1][0]) > .0001
            or abs(csp[0][1] - self.poly[-1][1]) > .0001
            or self.layer != self.layer_LWPOLY):
            self.LWPOLY_output()                            # terminate current polyline
            self.poly = [csp[0]]                            # initiallize new polyline
            self.color_LWPOLY = self.color
            self.layer_LWPOLY = self.layer
            self.closed_LWPOLY = self.closed
        self.poly.append(csp[1])
    def LWPOLY_output(self):
        if len(self.poly) == 1:
            return
        self.handle += 1
        self.dxf_add("  0\nLWPOLYLINE\n  5\n%x\n100\nAcDbEntity\n  8\n%s\n 62\n%d\n100\nAcDbPolyline\n 90\n%d\n 70\n%d\n" % (self.handle, self.layer_LWPOLY, self.color_LWPOLY, len(self.poly), self.closed_LWPOLY))
        for i in range(len(self.poly)):
            self.dxf_add(" 10\n%f\n 20\n%f\n 30\n0.0\n" % (self.poly[i][0],self.poly[i][1]))
    def dxf_spline(self,csp):
        knots = 8
        ctrls = 4
        self.handle += 1
        self.dxf_add("  0\nSPLINE\n  5\n%x\n100\nAcDbEntity\n  8\n%s\n 62\n%d\n100\nAcDbSpline\n" % (self.handle, self.layer, self.color))
        self.dxf_add(" 70\n8\n 71\n3\n 72\n%d\n 73\n%d\n 74\n0\n" % (knots, ctrls))
        for i in range(2):
            for j in range(4):
                self.dxf_add(" 40\n%d\n" % i)
        for i in csp:
            self.dxf_add(" 10\n%f\n 20\n%f\n 30\n0.0\n" % (i[0],i[1]))
    def ROBO_spline(self,csp):
        # this spline has zero curvature at the endpoints, as in ROBO-Master
        if (abs(csp[0][0] - self.csp_old[3][0]) > .0001
            or abs(csp[0][1] - self.csp_old[3][1]) > .0001
            or abs((csp[1][1]-csp[0][1])*(self.csp_old[3][0]-self.csp_old[2][0]) - (csp[1][0]-csp[0][0])*(self.csp_old[3][1]-self.csp_old[2][1])) > .001):
            self.ROBO_output()                              # terminate current spline
            self.xfit = array([csp[0][0]], float)           # initiallize new spline
            self.yfit = array([csp[0][1]], float)
            self.d = array([0], float)
            self.color_ROBO = self.color
            self.layer_ROBO = self.layer
        self.xfit = concatenate((self.xfit, zeros((3))))    # append to current spline
        self.yfit = concatenate((self.yfit, zeros((3))))
        self.d = concatenate((self.d, zeros((3))))
        for i in range(1, 4):
            j = len(self.d) + i - 4
            self.xfit[j] = get_fit(i/3.0, csp, 0)
            self.yfit[j] = get_fit(i/3.0, csp, 1)
            self.d[j] = self.d[j-1] + pointdistance((self.xfit[j-1],self.yfit[j-1]),(self.xfit[j],self.yfit[j]))
        self.csp_old = csp
    def ROBO_output(self):
        if len(self.d) == 1:
            return
        fits = len(self.d)
        ctrls = fits + 2
        knots = ctrls + 4
        self.xfit = concatenate((self.xfit, zeros((2))))    # pad with 2 endpoint constraints
        self.yfit = concatenate((self.yfit, zeros((2))))    # pad with 2 endpoint constraints
        self.d = concatenate((self.d, zeros((6))))          # pad with 3 duplicates at each end
        self.d[fits+2] = self.d[fits+1] = self.d[fits] = self.d[fits-1]
        solmatrix = zeros((ctrls,ctrls), dtype=float)
        for i in range(fits):
            solmatrix[i,i]   = get_matrix(self.d, i, i)
            solmatrix[i,i+1] = get_matrix(self.d, i, i+1)
            solmatrix[i,i+2] = get_matrix(self.d, i, i+2)
        solmatrix[fits, 0]   = self.d[2]/self.d[fits-1]     # curvature at start = 0
        solmatrix[fits, 1]   = -(self.d[1] + self.d[2])/self.d[fits-1]
        solmatrix[fits, 2]   = self.d[1]/self.d[fits-1]
        solmatrix[fits+1, fits-1] = (self.d[fits-1] - self.d[fits-2])/self.d[fits-1]   # curvature at end = 0
        solmatrix[fits+1, fits]   = (self.d[fits-3] + self.d[fits-2] - 2*self.d[fits-1])/self.d[fits-1]
        solmatrix[fits+1, fits+1] = (self.d[fits-1] - self.d[fits-3])/self.d[fits-1]
        xctrl = solve(solmatrix, self.xfit)
        yctrl = solve(solmatrix, self.yfit)
        self.handle += 1
        self.dxf_add("  0\nSPLINE\n  5\n%x\n100\nAcDbEntity\n  8\n%s\n 62\n%d\n100\nAcDbSpline\n" % (self.handle, self.layer_ROBO, self.color_ROBO))
        self.dxf_add(" 70\n0\n 71\n3\n 72\n%d\n 73\n%d\n 74\n%d\n" % (knots, ctrls, fits))
        for i in range(knots):
            self.dxf_add(" 40\n%f\n" % self.d[i-3])
        for i in range(ctrls):
            self.dxf_add(" 10\n%f\n 20\n%f\n 30\n0.0\n" % (xctrl[i],yctrl[i]))
        for i in range(fits):
            self.dxf_add(" 11\n%f\n 21\n%f\n 31\n0.0\n" % (self.xfit[i],self.yfit[i]))

    def process_shape(self, node, mat):
        nodetype = node.get(inkex.addNS("type","sodipodi"))
        if nodetype == "arc":
            # These are actually only used for checking the maths
            ui_arc = True
            ui_cx = float(node.get(inkex.addNS('cx','sodipodi')))
            ui_cy = float(node.get(inkex.addNS('cy','sodipodi')))
            ui_r = float(node.get(inkex.addNS('r','sodipodi'),0.0))
            ui_rx = float(node.get(inkex.addNS('rx','sodipodi'),ui_r))
            ui_ry = float(node.get(inkex.addNS('ry','sodipodi'),ui_r))
            ui_a0 = float(node.get(inkex.addNS('start','sodipodi'),0))
            ui_a1 = float(node.get(inkex.addNS('end','sodipodi'),2*math.pi))
        else:
            ui_arc = False

        rgb = (0,0,0)
        style = node.get('style')
        if style:
            style = simplestyle.parseStyle(style)
            if style.has_key('stroke'):
                if style['stroke'] and style['stroke'] != 'none' and style['stroke'][0:3] != 'url':
                    rgb = simplestyle.parseColor(style['stroke'])
        hsl = coloreffect.ColorEffect.rgb_to_hsl(coloreffect.ColorEffect(),rgb[0]/255.0,rgb[1]/255.0,rgb[2]/255.0)
        self.closed = 0                                 # only for LWPOLYLINE
        self.color = 7                                  # default is black
        if hsl[2]:
            self.color = 1 + (int(6*hsl[0] + 0.5) % 6)  # use 6 hues
        trans = node.get('transform')
        if trans:
            mat = simpletransform.composeTransform(mat, simpletransform.parseTransform(trans))
        if node.tag == inkex.addNS('path','svg'):
            d = node.get('d')
            if not d:
                inkex.errormsg("PATH DATA MISSING!")
                inkex.sys.exit()
                return
            # Filter out any eliptical arcs for special treatment:
            simplep = simplepath.parsePath(d)
            split = split_arc_nonarc(simplep)
            arc_simplep = split[1]
            simplep = split[0]
            if len(simplep)>0:
                if (simplep[-1][0] == 'z' or simplep[-1][0] == 'Z'):
                    self.closed = 1
                p = cubicsuperpath.CubicSuperPath(simplep)
                if (self.options.FLATTENBES):
                    cspsubdiv.cspsubdiv(p, self.options.flat)
                    np = []
                    for sp in p:
                        first = True
                        for csp in sp:
                            cmd = 'L'
                            if first:
                                cmd = 'M'
                            first = False
                            np.append([cmd,[csp[1][0],csp[1][1]]])
                    p = cubicsuperpath.parsePath(simplepath.formatPath(np))
                simpletransform.applyTransformToPath(mat, p)
                for sub in p:
                    for i in range(len(sub)-1):
                        s = sub[i]
                        e = sub[i+1]
                        if s[1] == s[2] and e[0] == e[1]:
                            if (self.options.POLY == 'true'):
                                self.LWPOLY_line([s[1],e[1]])
                            else:
                                self.dxf_line([s[1],e[1]])
                        elif (self.options.ROBO == 'true'):
                            self.ROBO_spline([s[1],s[2],e[0],e[1]])
                        else:
                            self.dxf_spline([s[1],s[2],e[0],e[1]])

            # Now process any arc segments:

            if len(arc_simplep) > 0:

                # As our path is broken by arcs, we cannot have a closed polyline:
                self.closed = 0

                i = 0
                while i < len(arc_simplep):
                    cmd, params = arc_simplep[i]
                    if cmd == 'M':
                        p0 = params[:]
                    else:
                        p1 = params[-2:]
                        rx,ry,theta,largearc,sweep = params[0:5]
                        e_params = convert_arc_abrxry0_to_crxry00102(p0,p1,rx,ry,theta,largearc==1,sweep==1)
                        cx,cy = e_params[0]
                        if (i<len(arc_simplep)-1):
                            cmd2, params2 = arc_simplep[i+1]
                        else:
                            cmd2 = '-'
                        if cmd2 == 'A' and params2[0:5] == params[0:5] and params2[-2:] == p0:
                            # complete circle or ellipse
                            a0 = 0
                            a1 = 2.0*math.pi
                            i = i + 1
                            p1 = p0
                        else:
                            a0 = e_params[4]
                            a1 = e_params[5]
                            p0 = p1
                        self.dxf_arc_transform(mat,cx,cy,rx,ry,theta,a0,a1)
                        # check did we get our maths right?
                        if ui_arc and ((abs(cx - ui_cx) > 0.05) or (abs(cy - ui_cy) > 0.05) or (abs(a0 - ui_a0)>0.1) or (abs(a1 - ui_a1)>0.1)):
                            inkex.errormsg("WARNING, Maths failure. Stored attributes of arc and calculated values do not agree!:")
                            inkex.errormsg("sodipodi:\tc=[%f,%f],r=[%f,%f],a0=%fpi,a1=%fpi" % (ui_cx,ui_cy,ui_rx,ui_ry,ui_a0/math.pi,ui_a1/math.pi))
                            inkex.errormsg("raw:\tc=[%f,%f],r=[%f,%f],a0=%fpi,a1=%fpi" % (cx,cy,rx,ry,a0/math.pi,a1/math.pi))
                    i = i+1

                return
        elif node.tag in [ inkex.addNS('circle','svg'), 'circle', \
                            inkex.addNS('ellipse','svg'), 'ellipse' ]:
                cx = float(node.get('cx',0))
                cy = float(node.get('cy',0))
                if node.tag == inkex.addNS('circle','svg'):
                    rx = float(node.get('r',0))
                    ry = rx
                else:
                    rx = float(node.get('rx',0))
                    ry = float(node.get('ry',rx))
                a0 = 0.0
                a1 = 2*math.pi
                self.dxf_arc_transform(mat,cx,cy,rx,ry,0,a0,a1)
                return
        elif node.tag == inkex.addNS('rect','svg'):
            self.closed = 1
            x = float(node.get('x'))
            y = float(node.get('y'))
            width = float(node.get('width'))
            height = float(node.get('height'))
            pt0 = [x,y]
            pt1 = [x + width, y]
            pt2 = [x + width, y + height]
            pt3 = [x, y + height]
            simpletransform.applyTransformToPoint(mat,pt0)
            simpletransform.applyTransformToPoint(mat,pt1)
            simpletransform.applyTransformToPoint(mat,pt2)
            simpletransform.applyTransformToPoint(mat,pt3)
            if (self.options.POLY == 'true'):
                self.LWPOLY_line([pt0,pt1])
                self.LWPOLY_line([pt1,pt2])
                self.LWPOLY_line([pt2,pt3])
                self.LWPOLY_line([pt3,pt0])
            else:
                self.dxf_line([pt0,pt1])
                self.dxf_line([pt1,pt2])
                self.dxf_line([pt2,pt3])
                self.dxf_line([pt3,pt0])
            return
        else:
            return

    def process_clone(self, node):
        trans = node.get('transform')
        x = node.get('x')
        y = node.get('y')
        mat = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        if trans:
            mat = simpletransform.composeTransform(mat, simpletransform.parseTransform(trans))
        if x:
            mat = simpletransform.composeTransform(mat, [[1.0, 0.0, float(x)], [0.0, 1.0, 0.0]])
        if y:
            mat = simpletransform.composeTransform(mat, [[1.0, 0.0, 0.0], [0.0, 1.0, float(y)]])
        # push transform
        if trans or x or y:
            self.groupmat.append(simpletransform.composeTransform(self.groupmat[-1], mat))
        # get referenced node
        refid = node.get(inkex.addNS('href','xlink'))
        refnode = self.getElementById(refid[1:])
        if refnode is not None:
            if refnode.tag == inkex.addNS('g','svg'):
                self.process_group(refnode)
            elif refnode.tag == inkex.addNS('use', 'svg'):
                self.process_clone(refnode)
            else:
                self.process_shape(refnode, self.groupmat[-1])
        # pop transform
        if trans or x or y:
            self.groupmat.pop()

    def process_group(self, group):
        if group.get(inkex.addNS('groupmode', 'inkscape')) == 'layer':
            style = group.get('style')
            if style:
                style = simplestyle.parseStyle(style)
                if style.has_key('display'):
                    if style['display'] == 'none' and self.options.layer_option and self.options.layer_option=='visible':
                        return
            layer = group.get(inkex.addNS('label', 'inkscape'))
            if self.options.layer_name and self.options.layer_option and self.options.layer_option=='name' and not layer.lower() in self.options.layer_name:
                return
              
            layer = layer.replace(' ', '_')
            if layer in self.layers:
                self.layer = layer
        trans = group.get('transform')
        if trans:
            self.groupmat.append(simpletransform.composeTransform(self.groupmat[-1], simpletransform.parseTransform(trans)))
        for node in group:
            if node.tag == inkex.addNS('g','svg'):
                self.process_group(node)
            elif node.tag == inkex.addNS('use', 'svg'):
                self.process_clone(node)
            else:
                self.process_shape(node, self.groupmat[-1])
        if trans:
            self.groupmat.pop()

    def effect(self):
        #Warn user if name match field is empty
        if self.options.layer_option and self.options.layer_option=='name' and not self.options.layer_name:
            inkex.errormsg(_("Error: Field 'Layer match name' must be filled when using 'By name match' option"))
            inkex.sys.exit()
        #Split user layer data into a list: "layerA,layerb,LAYERC" becomes ["layera", "layerb", "layerc"]
        if self.options.layer_name:
            self.options.layer_name = self.options.layer_name.lower().split(',')
			
        #References:   Minimum Requirements for Creating a DXF File of a 3D Model By Paul Bourke
        #              NURB Curves: A Guide for the Uninitiated By Philip J. Schneider
        #              The NURBS Book By Les Piegl and Wayne Tiller (Springer, 1995)
        # self.dxf_add("999\nDXF created by Inkscape\n")  # Some programs do not take comments in DXF files (KLayout 0.21.12 for example)
        self.dxf_add(dxf_templates.r14_header)
        for node in self.document.getroot().xpath('//svg:g', namespaces=inkex.NSS):
            if node.get(inkex.addNS('groupmode', 'inkscape')) == 'layer':
                layer = node.get(inkex.addNS('label', 'inkscape'))
                self.layernames.append(layer.lower())
                if self.options.layer_name and self.options.layer_option and self.options.layer_option=='name' and not layer.lower() in self.options.layer_name:
                    continue
                layer = layer.replace(' ', '_')
                if layer and not layer in self.layers:
                    self.layers.append(layer)
        self.dxf_add("  2\nLAYER\n  5\n2\n100\nAcDbSymbolTable\n 70\n%s\n" % len(self.layers))
        for i in range(len(self.layers)):
            self.dxf_add("  0\nLAYER\n  5\n%x\n100\nAcDbSymbolTableRecord\n100\nAcDbLayerTableRecord\n  2\n%s\n 70\n0\n  6\nCONTINUOUS\n" % (i + 80, self.layers[i]))
        self.dxf_add(dxf_templates.r14_style)

        scale = eval(self.options.units)
        if not scale:
            scale = 25.4/90     # if no scale is specified, assume inch as baseunit
        h = inkex.unittouu(self.document.getroot().xpath('@height', namespaces=inkex.NSS)[0])
        self.groupmat = [[[scale, 0.0, 0.0], [0.0, -scale, h*scale]]]
        doc = self.document.getroot()
        self.process_group(doc)
        if self.options.ROBO == 'true':
            self.ROBO_output()
        if self.options.POLY == 'true':
            self.LWPOLY_output()
        self.dxf_add(dxf_templates.r14_footer)
		#Warn user if layer data seems wrong
        if self.options.layer_name and self.options.layer_option and self.options.layer_option=='name':
            for layer in self.options.layer_name:
                if not layer in self.layernames:
                    inkex.errormsg(_("Warning: Layer '%s' not found!") % (layer))

if __name__ == '__main__':
    e = MyEffect()
    e.affect()


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
