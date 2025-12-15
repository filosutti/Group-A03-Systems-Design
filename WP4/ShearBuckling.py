import numpy as np
from math import pi
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from Spacing_Functions import rib_places

# -------------------------------------------------
# Wing constants
# -------------------------------------------------
wing_span = 23.78
half_wing_span = 11.89

c_r = 4.02
taper = 0.316
c_t = c_r * taper

n_ribs = int(input("Enter the number of ribs: "))

# -------------------------------------------------
# Spar geometry
# -------------------------------------------------
t_front = 0.012
t_rear = 0.012

spar_height_fraction_front = 0.115
spar_height_fraction_rear = 0.0743

# Normalized spar corner coordinates
c_1 = [0.25, 0.10399434]
c_2 = [0.25, -0.03497206]
c_3 = [0.75, 0.0637087]
c_4 = [0.75, -0.01024551]
corners_norm = np.array([c_1, c_3, c_4, c_2])

# -------------------------------------------------
# Material properties
# -------------------------------------------------
E = 70e9
nu = 0.33

# -------------------------------------------------
# Geometry functions
# -------------------------------------------------
def c(y):
    return c_r + (c_t - c_r) * (y / half_wing_span)

def spar_height_front(y):
    return spar_height_fraction_front * c(y)

def spar_height_rear(y):
    return spar_height_fraction_rear * c(y)

def Mean_Area(y):
    C = c(y)
    corners = corners_norm * C
    x = corners[:, 0]
    y_arr = corners[:, 1]
    area_enclosed = 0.5 * np.abs(
        np.dot(x, np.roll(y_arr, -1)) - np.dot(y_arr, np.roll(x, -1))
    )
    return area_enclosed

# -------------------------------------------------
# Loads (external modules)
# -------------------------------------------------
from sheardiagramPOSITIVEloadfactor import Shear
from torquediagrampositiveloadfactor import torque_pos_loadfactor

# -------------------------------------------------
# Buckling coefficient curves
# -------------------------------------------------
_ab_clamped = np.array([1 , 1.1 , 1.2 , 1.3 , 1.4 , 1.5 , 1.6 , 1.7 ,
                         2 , 2.25 , 2.5 , 3 , 3.25 , 3.5 , 3.75 , 4 ,
                         4.25 , 4.5 , 4.75 , 5])

_k_s_clamped = np.array([15 , 14 , 13 , 12 , 11.8 , 11.6 , 11.2, 11 ,
                          10.3 , 10 , 9.9 , 9.8 , 9.7 , 9.6 , 9.5 ,
                          9.5 , 9.5 , 9.5 , 9.5 , 9.5])

_ab_hinged = _ab_clamped.copy()

_k_s_hinged = np.array([10.7 , 9 , 8.4 , 7.5 , 7.3 , 7.1 , 6.8 , 6.6 ,
                         6.3 , 6.2 , 6 , 5.8 , 5.8 , 5.8 , 5.8 ,
                         5.7 , 5.6 , 5.58 , 5.56 , 5.54])

k_s_clamped_interp = PchipInterpolator(_ab_clamped, _k_s_clamped, extrapolate=True)
k_s_hinged_interp = PchipInterpolator(_ab_hinged, _k_s_hinged, extrapolate=True)

def tau_critical(k_s, E, nu, t, b):
    return (k_s * pi**2 * E * t**2) / (12 * (1 - nu**2) * b**2)

# -------------------------------------------------
# MAIN BUCKLING ANALYSIS
# -------------------------------------------------
def compute_spar_buckling(n_ribs):

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # LINEAR RIB SPACING (YOUR FUNCTION USED HERE)
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    initial_spacing = 0.25  # [m] – user-defined
    rib_positions, spacings = rib_places(
        initial_spacing,
        half_wing_span,
        n_ribs
    )
    panel_edges = rib_positions
    n_panels = n_ribs - 1
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    results = []
    y_plot = []
    MoS_front_plot = []
    MoS_rear_plot = []

    for i in range(n_panels):
        y0 = panel_edges[i]
        y1 = panel_edges[i + 1]
        a = y1 - y0

        y_samples = np.linspace(y0, y1, 150)

        # Loads
        V_samples = abs(np.array([Shear(y) for y in y_samples]))
        T_samples = abs(np.array([torque_pos_loadfactor(y) for y in y_samples]))
        V_max = np.max(V_samples)
        T_max = np.max(T_samples)

        # Geometry
        b_f = np.min(spar_height_front(y_samples))
        b_r = np.min(spar_height_rear(y_samples))
        A_min = np.min([Mean_Area(y) for y in y_samples])

        ab_f = a / b_f
        ab_r = a / b_r

        # Buckling coefficients
        k_s_f = k_s_hinged_interp(ab_f)
        k_s_r = k_s_hinged_interp(ab_r)
        bc = "pinned–pinned"

        # Shear stresses
        tau_trans = V_max / (b_f * t_front + b_r * t_rear)
        q_T = T_max / (2 * A_min)

        tau_t_front = q_T / t_front
        tau_t_rear = q_T / t_rear

        tau_max_front = abs(1.5 * tau_trans + tau_t_front)
        tau_max_rear = abs(1.5 * tau_trans - tau_t_rear)

        # Critical stresses
        tau_cr_f = tau_critical(k_s_f, E, nu, t_front, b_f)
        tau_cr_r = tau_critical(k_s_r, E, nu, t_rear, b_r)

        util_f = tau_cr_f / tau_max_front
        util_r = tau_cr_r / tau_max_rear

        results.append({
            "panel": i + 1,
            "bc": bc,
            "tau_max_front": tau_max_front,
            "tau_max_rear": tau_max_rear,
            "tau_cr_front": tau_cr_f,
            "tau_cr_rear": tau_cr_r,
            "util_front": util_f,
            "util_rear": util_r,
            "fails": (util_f < 1.0) or (util_r < 1.0)
        })

        MoS_front = abs(util_f - 1)
        MoS_rear = abs(util_r - 1)

        y_plot.extend(y_samples)
        MoS_front_plot.extend([MoS_front] * len(y_samples))
        MoS_rear_plot.extend([MoS_rear] * len(y_samples))

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(y_plot, MoS_front_plot, label="Front Spar MoS")
    plt.plot(y_plot, MoS_rear_plot, label="Rear Spar MoS")
    plt.axhline(0, color='k', linestyle='--')
    plt.xlabel("Spanwise Position y [m]")
    plt.ylabel("Margin of Safety")
    plt.title("Shear Buckling Margin of Safety Along Half Span")
    plt.grid(True)
    plt.legend()
    plt.show()

    return results

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    R = compute_spar_buckling(n_ribs)

    for r in R:
        print(f"\nPanel {r['panel']} ({r['bc']})")
        print(f" tau_max_front = {r['tau_max_front']:.1f} Pa")
        print(f" tau_max_rear = {r['tau_max_rear']:.1f} Pa")
        print(f" tau_cr_front = {r['tau_cr_front']:.1f}, util_front = {r['util_front']:.3f}")
        print(f" tau_cr_rear = {r['tau_cr_rear']:.1f}, util_rear = {r['util_rear']:.3f}")
        print(" Status:", "FAIL" if r["fails"] else "OK")
