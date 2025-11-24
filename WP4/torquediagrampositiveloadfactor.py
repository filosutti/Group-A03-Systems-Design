import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import math as m

# -----------------------------
# Load inputs
# -----------------------------
from TL import LperSpan0, MperSpan0

L = 11.89   # Half-span of the wing

# -----------------------------
# Aerodynamic moment arm: Distance between flexural axis and aerodynamic center
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
# Interpolated aerodynamic loads from XFLR5 data
# -----------------------------
Lift   = LperSpan0
Moment = MperSpan0  # Pitching moment distribution from XFLR5

# -----------------------------
# Distributed torque densities
# -----------------------------
def tau_l(x):
    return abs(Lift(x) * d(x))   # Positive torque (CCW) for positive lift (+g)

def tau_m(x):
    return abs(Moment(x))        # Positive torque (CCW); keep as provided

# -----------------------------
# Engine point torque
# -----------------------------
w_engine    = 4800 * 0.45359237 * 9.81   # N  
thrust_arm  = 2.32 + 0.3
engine_arm  = 2.495
x_engine    = 3.75

T_thrust = 83.1e3

MomentPoint = abs((w_engine * engine_arm) - (T_thrust * thrust_arm))

# -----------------------------
# Root torque T0 – ensures T(L)=0
# -----------------------------
def T0_calc():
    tl, _ = quad(tau_l, 0, L)
    tm, _ = quad(tau_m, 0, L)
    return tl + MomentPoint - tm

T0 = T0_calc()

# -----------------------------
# Internal torque distribution (RENAMED)
# -----------------------------
def torque_pos_loadfactor(x):
    tl, _ = quad(tau_l, 0, x)
    tm, _ = quad(tau_m, 0, x)
    tpoint = MomentPoint if x >= x_engine else 0.0
    return -T0 + tl - tm + tpoint

# -----------------------------
# Sanity checks
# -----------------------------
tl_total, _ = quad(tau_l, 0, L)
tm_total, _ = quad(tau_m, 0, L)

print("\n--- TORQUE SIGN CHECKS ---")
print(f"Engine weight moment (CCW +) : {w_engine * engine_arm: .1f} N·m")
print(f"Engine thrust moment (CW -)   : {T_thrust * thrust_arm: .1f} N·m")
print(f"MomentPoint (net engine)      : {MomentPoint: .1f} N·m")
print(f"Integral tau_l (0→L)          : {tl_total: .1f} N·m")
print(f"Integral tau_m (0→L)          : {tm_total: .1f} N·m")
print(f"T0 (root reaction)            : {T0: .1f} N·m")
print("Check: T0 + tl + tm + Mpt = ",
      T0 + tl_total + tm_total + MomentPoint)

# -----------------------------
# Plot internal torque diagram
# -----------------------------
x_vals = np.linspace(0, L, 400)
T_vals = np.array([torque_pos_loadfactor(xi) for xi in x_vals])

print(f"\nT(L) = {T_vals[-1]:.6f}   (should be 0)\n")

T_before = torque_pos_loadfactor(x_engine - 1e-6)
T_after  = torque_pos_loadfactor(x_engine + 1e-6)

plt.figure(figsize=(10, 6))
plt.plot(x_vals, T_vals / 1e3, label='Internal Torque T(x)', color='blue')
plt.plot([x_engine, x_engine], [T_before / 1e3, T_after / 1e3],
         color='red', linestyle='--', label='Engine Point Torque')
plt.scatter([x_engine], [T_after / 1e3], color='red')
plt.title('Internal Torque Distribution Along Wing Span')
plt.xlabel('Spanwise Location x (m)')
plt.ylabel('Internal Torque T(x) (kN·m)')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.legend()
plt.grid()
plt.show()
