import numpy as np
import matplotlib.pyplot as plt

from bendingdiagrampositiveload import M_pos_load
from centroid import calculate_wingbox_centroid

from TL import c





# ---------------------------------------------------------------------
# CONSTANTS & GEOMETRY (UPDATED FOR HARMONIZATION)
# ---------------------------------------------------------------------
G = 28e9 
E = 72.4e9 

#Stringer geometry
n_stringers_side = 14
L_stringer = 0.015           #0.25 of this offset to inside for centroid of point area of stringer
t_stringer = 1*(10**(-3))
A_stringer = (L_stringer * t_stringer)*2 - (t_stringer**2)  #approx area of L shape stringer

# Engine parameters (UNCHANGED)
w_engine  = 4800 * 0.45359237 * 9.81 
thrust_arm = 2.32 + 0.3
engine_arm = 2.495
x_engine  = 3.75 
T_thrust = 83.1e3

# Harmonized Wingbox section properties
t_skin = 0.003
rho_Al2024 = 2780
coords_unscaled = [(0.2, -0.02723), (0.7, -0.0066), (0.7, 0.0666), (0.2, 0.08737)] # FB, RB, RT, FT




# Distributed Weight/Fuel Loads (UNCHANGED)
g = 9.81
W_engine_NOLOAD = 2177.243 * g

def Heaviside(x, x0):
 return 1.0 if x >= x0 else 0.0

def WeightDistribution(x): # Negative value means downward force
    return ((7*x)-821.693393608074)

def FuelDistribution(x):
 return 10*x-9148.6175 

# Aerodynamic moment arm (UNCHANGED)
def d(x):
    c_r = 4.02
    span = L
    taper = 0.316
    c_t = c_r * taper
    chord = c_r - (c_r - c_t) * (x / span)
    return 0.20 * chord

# ---------------------------------------------------------------------
# SECTION 1: CENTROID & INERTIA CALCULATION (UPDATED)
# ---------------------------------------------------------------------
# Re-using the provided calculate_wingbox_centroid (though it's complex)
from centroid import calculate_wingbox_centroid

def inertia_calculation(z):
    from TL import c
    c_z = c(z)
    
    # Centroid Calculation (Uses UNIFIED stringer list)
    cx, cy, stringer_coords = calculate_wingbox_centroid(coords_unscaled, t_skin, rho_Al2024, n_stringers_side, A_stringer, L_stringer)
    ce = (c_z * cx, c_z * cy)
    
    x_frac = [0.2, 0.7, 0.7, 0.2]
    y_frac = [-0.02723, -0.0066, 0.0666, 0.08737]
    x_scaled = [xf * c_z for xf in x_frac]
    y_scaled = [yf * c_z for yf in y_frac]
    
    # Torsional Constant J (Bredt's Theory) - UNCHANGED
    Am = 0.5 * np.abs(np.sum(np.array(x_scaled) * np.roll(np.array(y_scaled), -1) - 
                             np.roll(np.array(x_scaled), -1) * np.array(y_scaled)))
    perimeter_integral = 0
    t = t_skin*c_z
    for i in range(len(x_scaled)):
        x1, y1 = x_scaled[i], y_scaled[i]
        x2, y2 = x_scaled[(i + 1) % len(x_scaled)], y_scaled[(i + 1) % len(x_scaled)]
        l = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        perimeter_integral += l / t 
    J = (4 * Am**2) / perimeter_integral

    # Bending Inertias
    x_temp, y_temp = x_scaled + [x_scaled[0]], y_scaled + [y_scaled[0]]
    Ixxtot = Iyytot = Ixytot = 0
    
    # 1. Skin Contributions
    for i in range(len(x_temp)-1):
        dx, dy = x_temp[i+1]-x_temp[i], y_temp[i+1]-y_temp[i]
        l = np.sqrt(dx**2 + dy**2)
        A = l*t
        d_y = x_temp[i] + dx/2 - ce[0]
        d_x = y_temp[i] + dy/2 - ce[1]
        
        Ixx = (t*(l**3)*(dy/l)**2)/12 + A*(d_x**2)
        Iyy = (t*(l**3)*(dx/l)**2)/12 + A*(d_y**2)
        Ixy = (t*(l**3)*(dx*dy)/(l**2))/12 + A*(d_x*d_y)

        Ixxtot += Ixx
        Iyytot += Iyy
        Ixytot += Ixy
    
    # 2. Harmonized Stringer Contributions
    for sx_f, sy_f in stringer_coords:
        sx, sy = sx_f * c_z, sy_f * c_z
        A_str = A_stringer * (c_z)**2
        
        # NOTE: Stringer area should be considered constant or scale by (chord/chord_root)^2
        # For this context, let's keep A_str_f constant, only coordinates scale:
        
        d_y2 = sx - ce[0] # Horizontal distance from centroid
        d_x2 = sy - ce[1] # Vertical distance from centroid
        
        Ixxtot += A_str * d_x2**2
        Iyytot += A_str * d_y2**2
        Ixytot += A_str * d_x2 * d_y2
    return Ixxtot, Iyytot, Ixytot, J

def sigma_distribution(y,h):
    Ixx, Iyy, Ixy, J = inertia_calculation(y)
    Mx = M_pos_load(y)

    sigma_comp = Mx*h/Ixx
    return sigma_comp
