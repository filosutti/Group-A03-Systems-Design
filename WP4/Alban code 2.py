#Input: Wing Box Geometry
#Output: Wing Box Centroid

import numpy as np
import math
import matplotlib.pyplot as plt

print("i love kyrgyzstan")

corner = [(0,0), (4,0), (3,2), (1,2)]

def WingBoxCentroid(corner):
    cx = (corner[0][0] + corner[1][0] + corner[2][0] + corner[3][0]) / 4
    cy = (corner[0][1] + corner[1][1] + corner[2][1] + corner[3][1]) / 4
    print("Coordinates (x, y) of wing box centroid: (", cx, ",", cy, ")")
    return cx, cy

WingBoxCentroid(corner)