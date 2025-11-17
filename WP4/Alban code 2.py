#Input: Wing Box Geometry
#Output: Wing Box Centroid

import numpy as np
import math
import matplotlib.pyplot as plt

print("i love kyrgyzstan")

# corner inputs (temporary)
corner = []
corners = 4
for i in range(corners):
    print(f"Enter coordinates for corner {i+1}:")
    x = float(input("  x: "))
    y = float(input("  y: "))
    corner.append((x, y))

def WingBoxCentroid(corner):
    cx = (corner[0][0] + corner[1][0] + corner[2][0] + corner[3][0]) / corners
    cy = (corner[0][1] + corner[1][1] + corner[2][1] + corner[3][1]) / corners
    print("Coordinates (x, y) of wing box centroid: (", cx, ",", cy, ")")
    return cx, cy

WingBoxCentroid(corner)