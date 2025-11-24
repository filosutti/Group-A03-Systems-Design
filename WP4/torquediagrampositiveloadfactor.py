import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math as m


# -----------------------------
# Load inputs
# -----------------------------
from TL import LperSpan0, MperSpan0


L = 11.89   #Half-span of the wing

# -----------------------------
# Aerodynamic moment arm: Distanec between flexural axis and aerodynamic center
# CCW = +
# -----------------------------
def d(x):
    c_r = 4.02
    span = 11.89
    taper = 0.316

    c_t = c_r * taper
    chord = c_r - (c_r - c_t) * (x / span)
    return 0.20 * chord


# -----------------------------
# Interpolated aerodynamic loads from XLRF5 data
# -----------------------------
Lift   =  LperSpan0
Moment = MperSpan0 # This is the pitching moment distribution function in N, data from XFLR5

# -----------------------------
# Distributed torque densities
# -----------------------------
def tau_l(x):
    return abs(Lift(x) * d(x))     #Distributed torque due to lift about the flexural axis, unit N

def tau_m(x):
    return abs(Moment(x))        #Distributed pitching moment about the flexural axis, unit N

# -----------------------------
# Engine point torque (forces → moment about elastic axis)
# -----------------------------
w_engine    = 4800 * 0.45359237 * 9.81   # N  
thrust_arm  = 2.32 + 0.3                  # m, take nacelle height divided by 2, that is the point of application
engine_arm  = 2.495                      # m, distance from the flexural axis to the engine CG
x_engine    = 3.75                      # m, position of the engine on the flexural axis, or distance from the root. 

T_thrust = 83.1e3 

# engine weight = CCW (+)
# thrust       = CW  (–)
MomentPoint = abs((w_engine * engine_arm) - (T_thrust * thrust_arm))

# -----------------------------
# Root torque T0 – ensures T(L)=0
# -----------------------------
def T0_calc():
    tl, _ = quad(tau_l, 0, L) #Quad integrats tau_l from 0 to L
    tm, _ = quad(tau_m, 0, L) #Quad integrats tau_m from 0 to L
    return tl+MomentPoint - tm

T0 = T0_calc()

# -----------------------------
# Internal torque distribution
# -----------------------------
def T(x):
    tl, _ = quad(tau_l, 0, x)   # integrate tau_l from 0 to x to get the torque as a function of spanwise coordinate
    tm, _ = quad(tau_m, 0, x)    # integrate tau_m from 0 to x to get the torque as a function of spanwise coordinate
    tpoint = MomentPoint if x >= x_engine else 0.0  # Point torque of the engine at x_engine
    return -T0 + tl - tm + tpoint                   # Total internal torque distribution

# -----------------------------
# Sanity checks for torque, does it make sense?
# -----------------------------
tl_total, _ = quad(tau_l, 0, L)
tm_total, _ = quad(tau_m, 0, L)

#print("\n--- TORQUE SIGN CHECKS ---")
#print(f"Engine weight moment (CCW +) : {w_engine * engine_arm: .1f} N·m")
#print(f"Engine thrust moment (CW -)   : {T_thrust * thrust_arm: .1f} N·m")
#print(f"MomentPoint (net engine)      : {MomentPoint: .1f} N·m   (negative = CW)")
#print(f"Integral tau_l (0→L)          : {tl_total: .1f} N·m")
#print(f"Integral tau_m (0→L)          : {tm_total: .1f} N·m")
#print(f"T0 (root reaction)            : {T0: .1f} N·m")
#print("Check: T0 + tl + tm + Mpt = ",
#      T0 + tl_total + tm_total + MomentPoint)

# -----------------------------
# Plot internal torque diagram
# -----------------------------
#x_vals = np.linspace(0, L, 400)   # X positions from root to tip
#T_vals = np.array([T(xi) for xi in x_vals])  # Corresponding torque values

#print(f"\nT(L) = {T_vals[-1]:.6f}   (should be 0)\n")

# Engine jump (for plotting the point moment)  
#T_before = T(x_engine - 1e-6)
#T_after  = T(x_engine + 1e-6)

# -----------------------------
# Plot
# -----------------------------

#plt.figure(figsize=(10, 6))
#plt.plot(x_vals, T_vals / 1e3, label='Internal Torque T(x)', color='blue')
#plt.plot([x_engine, x_engine], [T_before / 1e3, T_after / 1e3], color='red', linestyle='--', label='Engine Point Torque')
#plt.scatter([x_engine], [T_after / 1e3], color='red')  # Mark the point after the jump
#plt.title('Internal Torque Distribution Along Wing Span')
#plt.xlabel('Spanwise Location x (m)')
#plt.ylabel('Internal Torque T(x) (kN·m)')
#plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
#plt.legend()
#plt.grid()
#plt.show()

