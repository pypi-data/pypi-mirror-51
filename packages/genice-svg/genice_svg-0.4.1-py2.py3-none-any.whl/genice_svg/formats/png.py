# coding: utf-8
"""
GenIce format plugin to generate a PNG file.

Usage:
    % genice CS2 -r 3 3 3 -f png[shadow:bg=#f00] > CS2.png
	
Options:
    rotatex=30
    rotatey=30
    rotatez=30
    shadow         Draw shadows behind balls.
    bg=#f00        Specify the background color.
    H=0            Size of the hydrogen atom
    O=0.06
    HB=0.4
    OH=0.5
"""


desc = { "ref": {},
         "brief": "PNG (Portable Network Graphics).",
         "usage": __doc__,
         }


import re
from math import sin, cos, pi
import numpy as np

from genice_svg import hooks
from genice_svg.render_png import Render

    
def hook0(lattice, arg):
    lattice.logger.info("Hook0: ArgParser.")
    lattice.poly     = False # unavailable for PNG
    lattice.renderer = Render
    lattice.shadow   = None
    lattice.oxygen   = 0.06 # absolute radius in nm
    lattice.HB       = 0.4  # radius relative to the oxygen
    lattice.OH       = 0.5  # radius relative to the oxygen
    lattice.hydrogen = 0    # radius relative to the oxygen
    lattice.arrows   = False # always false for png
    lattice.bgcolor  = '#fff'
    lattice.proj = np.array([[1., 0, 0], [0, 1, 0], [0, 0, 1]])
    if arg == "":
        pass
        #This is default.  No reshaping applied.
    else:
        args = arg.split(":")
        for a in args:
            if a.find("=") >= 0:
                key, value = a.split("=")
                lattice.logger.info("  Option with arguments: {0} := {1}".format(key,value))
                if key == "rotmat":
                    value = re.search(r"\[([-0-9,.]+)\]", value).group(1)
                    lattice.proj = np.array([float(x) for x in value.split(",")]).reshape(3,3)
                elif key == "rotatex":
                    value = float(value)*pi/180
                    cosx = cos(value)
                    sinx = sin(value)
                    R = np.array([[1, 0, 0], [0, cosx, sinx], [0,-sinx, cosx]])
                    lattice.proj = np.dot(lattice.proj, R)
                elif key == "rotatey":
                    value = float(value)*pi/180
                    cosx = cos(value)
                    sinx = sin(value)
                    R = np.array([[cosx, 0, -sinx], [0, 1, 0], [sinx, 0, cosx]])
                    lattice.proj = np.dot(lattice.proj, R)
                elif key == "rotatez":
                    value = float(value)*pi/180
                    cosx = cos(value)
                    sinx = sin(value)
                    R = np.array([[cosx, sinx, 0], [-sinx, cosx, 0], [0, 0, 1]])
                    lattice.proj = np.dot(lattice.proj, R)
                elif key == "shadow":
                    lattice.shadow = value
                elif key == "H":
                    lattice.hydrogen = float(value)
                elif key == "HB":
                    lattice.HB = float(value)
                elif key == "O":
                    lattice.oxygen = float(value)
                elif key == "OH":
                    lattice.OH = float(value)
                elif key == "bg":
                    lattice.bgcolor = value
            else:
                lattice.logger.info("  Flags: {0}".format(a))
                if a == "shadow":
                    lattice.shadow = "#8881"
                elif a == "H":
                    lattice.hydrogen = 0.6
                    lattice.HB = 0.2
                elif a == "OH":
                    lattice.OH = 0.5
                else:
                    assert False, "  Wrong options."
    lattice.logger.info("Hook0: end.")




hooks = {0:hook0, 2:hooks.hook2, 6:hooks.hook6}

