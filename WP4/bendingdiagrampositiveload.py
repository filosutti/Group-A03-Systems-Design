
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid


# -----------------------------
# Import V(x) and geometry from shear file
# -----------------------------
from sheardiagramPOSITIVEloadfactor import Shear
L = 11.89  # half Wing span in meters
x_engine = 3.75
# -----------------------------
# Vectorized x positions from tip to root to have M_tip = 0
# -----------------------------
x_vals = np.linspace(L, 0, 400) # integrate from tip
V_vals = np.array([Shear(x) for x in x_vals])


T = 81e3          # thrust load [kN or kN-equivalent]
lambda_c = 3.3       # inflow angle [rad]
h_engine = 2.32 + 0.3      # engine vertical offset [m]

# Compute moment applied at engine
M_T = T * np.sin(np.radians(lambda_c)) * h_engine   # [kN·m]

# -----------------------------
# Bending moment M(x) via cumulative trapezoidal integration
# -----------------------------
M_vals = cumulative_trapezoid(V_vals, x_vals, initial=0)

# We integrated from tip → root, so x_vals decreases.
# The moment jump must be added to all points root-wards from x_engine:
M_vals += M_T * (x_vals <= x_engine)

# Reverse arrays to plot from root to tip
x_vals = x_vals[::-1]
M_vals = M_vals[::-1]


M_0 = M_vals[0]
M_max = min(M_vals)
print(f"Root bending moment M_0 = {M_0:.3f} kN·m")


def M_pos_load(x):
    return float(np.interp(x, x_vals, M_vals))

# -----------------------------------------
# Fit a polynomial to M(x)
# -----------------------------------------
degree = 5   # choose polynomial degree (try 3–7)
coeffs = np.polyfit(x_vals, M_vals, degree)

# Convert to a polynomial object for easy evaluation
M_poly = np.poly1d(coeffs)

print("Polynomial coefficients (highest degree first):")
print(coeffs)

print("\nM(x) = ")
print(M_poly)
# -----------------------------
# Plot Bending Moment
# -----------------------------
plt.figure(figsize=(10,5))
plt.plot(x_vals, M_vals, linewidth=2, label='Bending Moment M(x)')
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(x_engine, color='red', linestyle='--', label='Engine Location')
plt.xlabel('x [m] from root')
plt.ylabel('Bending Moment for positive load factor M(x) [N·m]')
plt.title('Bending Moment Diagram (Zero at Tip)')
plt.grid(True)
plt.legend()
plt.show()

