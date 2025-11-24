#DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE
#DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE
#DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE
#DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE DONT USE

import numpy as np
import math
import matplotlib.pyplot as plt

########## temporary ##########
# wing box skin inputs (must be in order)
corners = 4
corner = []
skinThickness = float(input("Enter the skin thickness (m): "))
skinDensity = float(input("Enter the skin density (kg/m^3): "))

for i in range(corners):
    print(f"Enter coordinates for corner {i+1}:")
    xc = float(input("  x: "))
    yc = float(input("  y: "))
    corner.append((xc, yc))

# stringer inputs
stringers = []
nStringers = int(input("Enter number of stringers (point areas): "))
stringerDensity = float(input("Enter stringer density (kg/m^3): "))

for i in range(nStringers):
    print(f"Enter data for stringer {i+1}:")
    xa = float(input("  x: "))
    ya = float(input("  y: "))
    area = float(input("  effective area (m^2): "))
    stringers.append((xa, ya, area, stringerDensity))
##########  temporary  ##########



def WingBoxCentroid(corner, skinThickness, skinDensity, stringers=[]):
    # Close the loop
    x = [p[0] for p in corner] + [corner[0][0]]
    y = [p[1] for p in corner] + [corner[0][1]]

    # Compute polygon area
    A = 0
    Cx = 0
    Cy = 0
    for i in range(4):
        cross = x[i]*y[i+1] - x[i+1]*y[i]
        A += cross
        Cx += (x[i] + x[i+1]) * cross
        Cy += (y[i] + y[i+1]) * cross
    A *= 0.5
    if abs(A) < 0.000001:
        raise ValueError("Polygon area zero or polygon is degenerate")
    Cx /= (6*A)
    Cy /= (6*A)

    # Skin mass (area times thickness times density)
    m_skin = abs(A) * skinThickness * skinDensity

    # Start mass sums
    sum_mx = m_skin * Cx
    sum_my = m_skin * Cy
    total_mass = m_skin

    # Add stringers (point areas)
    for s in stringers:
        xs, ys, area, density = s
        m = area * density
        sum_mx += m * xs
        sum_my += m * ys
        total_mass += m

    # Total centroid
    xc = sum_mx / total_mass
    yc = sum_my / total_mass

    # Return centroid
    c = [xc, yc]
    return c

centroid = WingBoxCentroid(corner, skinThickness, skinDensity, stringers)
print("Wing box centroid:", centroid)
