import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import math as m
from scipy.interpolate import interp1d

# -----------------------------
# Wing geometry
# -----------------------------
S_wing = 62.83 
AR = 10.44
b_w = 23.78
c_r = 4.02
c_t = 1.27 
MAC = 2.88
taper = 0.316
Weight_engine_arm = 2.495
T_thrust = 83.1e3  # N
Thrust_engine_arm = 2.32 + 0.3  # m
Spanwise_position_engine = 3.75  # m
n_negative = -1
n_positive = 2.5



# -----------------------------
# Load inputs
# -----------------------------
from XLRF5_data import ylst0, LperSpan0, MperSpan0

ygrid0 = ylst0
L = ygrid0.max()

# -----------------------------
# Torque arm
# -----------------------------
def d(y): #moment arm for the aerodynamic lift
    span = b_w/2
    c_t = c_r * taper
    chord = c_r - (c_r - c_t) / span * y
    return 0.25 * chord #TBD


# -----------------------------
# Interpolated loads
# -----------------------------
Lift   = interp1d(ygrid0, LperSpan0, kind='cubic', fill_value='extrapolate')
Moment = interp1d(ygrid0, MperSpan0, kind='cubic', fill_value='extrapolate')

# -----------------------------
# Distributed torque densities
# CW = negative
# -----------------------------
def tau_l(y):
    return -Lift(y) * d(y)     # CW

def tau_m(y):
    return -Moment(y)          # CW

# -----------------------------
# Engine point torque (same direction = CW = negative)
# -----------------------------
wengine = 4800 * 0.45359237 * 9.81   # N

# engine weight = CCW = positive
# thrust = CW = negative
# 👉 but your FBD states the RESULTANT engine point moment acts CW
MomentPoint = -(wengine * Weight_engine_arm - T_thrust * Thrust_engine_arm)   # FORCE it CW

# -----------------------------
# Compute root torque T0 (CCW positive)
# -----------------------------
def T0_calc():
    tl, _ = quad(tau_l, 0, L)
    tm, _ = quad(tau_m, 0, L)
    return -(tl + tm + MomentPoint)

T0 = T0_calc()

# -----------------------------
# Internal torque distribution
# -----------------------------
def T(y):
    tl, _ = quad(tau_l, 0, y)
    tm, _ = quad(tau_m, 0, y)
    tpoint = MomentPoint if y >= Spanwise_position_engine else 0.0
    return T0 + tl + tm + tpoint

# -----------------------------
# Plot
# -----------------------------
y_vals = np.linspace(0, L, 400)
T_vals = np.array([T(xi) for xi in y_vals])

print(f"T0 = {T0:.3f}  N·m")
print(f"T(L) = {T_vals[-1]:.6f} (should be 0)")

plt.figure(figsize=(10,5))
plt.plot(y_vals, T_vals, lw=2)
plt.axhline(0, color='black')
plt.axvline(Spanwise_position_engine, color='red', linestyle='--', label='Engine')
plt.title("Correct Torque Diagram (matches FBD)")
plt.xlabel("Span y [m]")
plt.ylabel("Torque T(y) [N·m]")
plt.grid(True)
plt.legend()
plt.show()