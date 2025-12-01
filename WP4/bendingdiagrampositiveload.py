
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


# -----------------------------
# Bending moment M(x) via cumulative trapezoidal integration
# -----------------------------
M_vals = cumulative_trapezoid(V_vals, x_vals, initial=0)


# Reverse arrays to plot from root to tip
x_vals = x_vals[::-1]
M_vals = M_vals[::-1]

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
plt.ylabel('Bending Moment for Positive load factor M(x) [N·m]')
plt.title('Bending Moment Diagram (Zero at Tip)')
plt.grid(True)
plt.legend()
plt.show()