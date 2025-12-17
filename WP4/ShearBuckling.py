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
initial_spacing = float(input("Enter the initial rib spacing at the root [m]: "))

# -------------------------------------------------
# Spar geometry
# -------------------------------------------------
t_front = float(input("Enter front spar thickness [m]: "))
t_rear = t_front

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
E = 72.4e9
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
    return 0.5 * abs(np.dot(x, np.roll(y_arr, -1)) -
                     np.dot(y_arr, np.roll(x, -1)))

# -------------------------------------------------
# Loads
# -------------------------------------------------
from sheardiagramPOSITIVEloadfactor import Shear
from torquediagrampositiveloadfactor import torque_pos_loadfactor

# -------------------------------------------------
# Buckling coefficients
# -------------------------------------------------
_ab = np.array([1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,
                2,2.25,2.5,3,3.25,3.5,3.75,4,
                4.25,4.5,4.75,5])

_k_s = np.array([10.7,9,8.4,7.5,7.3,7.1,6.8,6.6,
                 6.3,6.2,6,5.8,5.8,5.8,5.8,
                 5.7,5.6,5.58,5.56,5.54])

k_s_interp = PchipInterpolator(_ab, _k_s, extrapolate=True)

def tau_critical(k_s, E, nu, t, b):
    return (k_s * pi**2 * E * t**2) / (12 * (1 - nu**2) * b**2)

# -------------------------------------------------
# Buckling analysis (returns panel results + MoS plots)
# -------------------------------------------------
def compute_spar_buckling_from_ribs(rib_positions):

    panel_results = []
    y_plot, MoS_f_plot, MoS_r_plot = [], [], []

    for i in range(len(rib_positions) - 1):

        y0, y1 = rib_positions[i], rib_positions[i+1]
        a = y1 - y0
        y = np.linspace(y0, y1, 120)

        V = np.max(np.abs([Shear(yy) for yy in y]))
        T = np.max(np.abs([torque_pos_loadfactor(yy) for yy in y]))

        b_f = np.min(spar_height_front(y))
        b_r = np.min(spar_height_rear(y))
        A = np.min([Mean_Area(yy) for yy in y])

        ab_f = a / b_f
        ab_r = a / b_r

        k_f = k_s_interp(ab_f)
        k_r = k_s_interp(ab_r)

        tau_trans = V / (b_f * t_front + b_r * t_rear)
        q_T = T / (2 * A)

        tau_f = abs(1.5 * tau_trans + q_T / t_front)
        tau_r = abs(1.5 * tau_trans - q_T / t_rear)

        tau_cr_f = tau_critical(k_f, E, nu, t_front, b_f)
        tau_cr_r = tau_critical(k_r, E, nu, t_rear, b_r)

        util_f = tau_cr_f / tau_f
        util_r = tau_cr_r / tau_r

        panel_results.append({
            "panel": i + 1,
            "util_front": util_f,
            "util_rear": util_r,
            "status": "OK" if (util_f >= 1 and util_r >= 1) else "FAIL"
        })

        MoS_f = abs(util_f - 1)
        MoS_r = abs(util_r - 1)

        y_plot.extend(y)
        MoS_f_plot.extend([MoS_f] * len(y))
        MoS_r_plot.extend([MoS_r] * len(y))

    return panel_results, y_plot, MoS_f_plot, MoS_r_plot

# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":

    # -------- Variable spacing
    ribs_var, _ = rib_places(initial_spacing, half_wing_span, n_ribs)
    res_var, y_v, MoS_f_v, MoS_r_v = compute_spar_buckling_from_ribs(ribs_var)

    # -------- Equal spacing
    ribs_eq = np.linspace(0, half_wing_span, n_ribs)
    res_eq, y_e, MoS_f_e, MoS_r_e = compute_spar_buckling_from_ribs(ribs_eq)

    # -------- Print panel results
    print("\nVARIABLE (ROOT-BASED) SPACING RESULTS")
    for r in res_var:
        print(f" Panel {r['panel']:2d} | "
              f"util_f = {r['util_front']:.2f} | "
              f"util_r = {r['util_rear']:.2f} | {r['status']}")

    print("\nEQUAL SPACING RESULTS")
    for r in res_eq:
        print(f" Panel {r['panel']:2d} | "
              f"util_f = {r['util_front']:.2f} | "
              f"util_r = {r['util_rear']:.2f} | {r['status']}")

    # -------- Plot MoS comparison
    plt.figure(figsize=(10,5))

    plt.plot(y_v, MoS_f_v, 'b-', label="Front – Variable spacing")
    plt.plot(y_v, MoS_r_v, 'r-', label="Rear – Variable spacing")

    plt.plot(y_e, MoS_f_e, 'b--', label="Front – Equal spacing")
    plt.plot(y_e, MoS_r_e, 'r--', label="Rear – Equal spacing")

    plt.axhline(0, color='k', linestyle='--')
    plt.xlabel("Spanwise Position y [m]")
    plt.ylabel("Margin of Safety")
    plt.title("Shear Buckling Margin of Safety Comparison")
    plt.grid(True)
    plt.legend()
    plt.show()




#DESIGNS THAT WORK:

# DESIGN 1: 12 STRINGERS (per side), w_stringer = 15c, t_stringer = 4 mm, t_skin = 6 mm , t_spar = 9 mm
# 
# DESIGN 3: 6 STRINGERS (per side), w_stringer = 15c, t_stringer = 4 mm, t_skin = 12 mm , t_spar = 12 mm

#DESIGNS THAT DONT WORK:


# DESIGN 2: 6 STRINGERS (per side), w_stringer = 20c, t_stringer = 8 mm, t_skin = 6 mm , t_spar = 6 mm