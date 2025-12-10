import numpy as np
from math import pi
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt

# Constants of the wing
wing_span = 23.78  # meters
half_wing_span = 11.89  # meters
c_r = 4.02
taper = 0.316
c_t = c_r * taper
n_ribs = 22  # THIS IS AN INPUT
t_front = 0.00603  # front spar thickness [m]
t_rear = 0.00603  # rear spar thickness [m]
spar_height_fraction_front = 1.5
spar_height_fraction_rear = 1.5

# Normalized spar corner coordinates
c_1 = [0.25, 0.10399434]
c_2 = [0.25, -0.03497206]
c_3 = [0.75, 0.0637087]
c_4 = [0.75, -0.01024551]
corners_norm = np.array([c_1, c_3, c_4, c_2])

# Material properties
E = 70e9  # Pa
nu = 0.33

# Geometric functions
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
    area_enclosed = 0.5 * np.abs(np.dot(x, np.roll(y_arr, -1)) - np.dot(y_arr, np.roll(x, -1)))
    return area_enclosed

# Shear force and torque functions
from sheardiagramPOSITIVEloadfactor import Shear
from torquediagrampositiveloadfactor import torque_pos_loadfactor

# k_s curves
_ab_clamped = np.array([1 , 1.1 , 1.2 , 1.3 , 1.4 , 1.5 , 1.6 , 1.7 , 2 , 2.25 , 2.5 , 3 , 3.25 , 3.5 , 3.75 , 4 , 4.25 , 4.5 , 4.75 , 5])
_k_s_clamped = np.array([15 , 14 , 13 , 12 , 11.8 , 11.6 , 11.2, 11 , 10.3 , 10 , 9.9 , 9.8 , 9.7 , 9.6 , 9.5 , 9.5 , 9.5 , 9.5 , 9.5 , 9.5])
_ab_hinged = np.array([1 , 1.1 , 1.2 , 1.3 , 1.4 , 1.5 , 1.6 , 1.7 , 2 , 2.25 , 2.5 , 3 , 3.25 , 3.5 , 3.75 , 4 , 4.25 , 4.5 , 4.75 , 5])
_k_s_hinged = np.array([10.7 , 9 , 8.4 , 7.5 , 7.3 , 7.1 , 6.8 , 6.6 , 6.3 , 6.2 , 6 , 5.8 , 5.8 , 5.8 , 5.8 , 5.7 , 5.6 , 5.58 , 5.56 , 5.54])
k_s_clamped_interp = PchipInterpolator(_ab_clamped, _k_s_clamped, extrapolate=True)
k_s_hinged_interp = PchipInterpolator(_ab_hinged, _k_s_hinged, extrapolate=True)

def k_s_clamped_from_ab(ab):
    return k_s_clamped_interp(ab)

def k_s_hinged_from_ab(ab):
    return k_s_hinged_interp(ab)

def tau_critical(k_s, E, nu, t, b):
    return (k_s * (np.pi**2) * E * t**2) / (12 * (1 - nu**2) * b**2)

# MAIN FUNCTION
def compute_spar_buckling(n_ribs):
    n_bays = n_ribs - 1
    panel_edges = np.linspace(0.0, half_wing_span, n_bays + 1)
    results = []

    y_plot = []
    MoS_front_plot = []
    MoS_rear_plot = []

    for i in range(n_bays):
        y0, y1 = panel_edges[i], panel_edges[i + 1]
        a_bay = y1 - y0

        y_samples = np.linspace(y0, y1, 20)
        V_samples = np.array([Shear(y) for y in y_samples])
        V_max = np.max(V_samples)
        T_samples = np.array([torque_pos_loadfactor(y) for y in y_samples])
        T_max = np.max(T_samples)

        b_f_min = np.min([spar_height_front(y) for y in y_samples])
        b_r_min = np.min([spar_height_rear(y) for y in y_samples])

        ab_f = a_bay / b_f_min
        ab_r = a_bay / b_r_min

        if i == 0:
            bc = "clamped"
            k_s_f = 8.98 + 5.61 / (ab_f*2) - 1.99/ (ab_f*3)
            k_s_r = 8.98 + 5.61 / (ab_r*2) - 1.99/ (ab_r*3)
        else:
            bc = "hinged"
            k_s_f = 5.34 + 4.0 / (ab_f**2)
            k_s_r = 5.34 + 4.0 / (ab_r**2)

        A_samples = [Mean_Area(y) for y in y_samples]
        A_min = np.min(A_samples)

        tau_transverse = V_max / (b_f_min * t_front + b_r_min * t_rear)
        q_T = T_max / (2 * A_min)
        tau_torque_front = q_T / t_front
        tau_torque_rear = q_T / t_rear
        tau_max_front = 1.5 * tau_transverse + abs(tau_torque_front)
        tau_max_rear = 1.5 * tau_transverse + abs(tau_torque_rear)

        tau_cr_f = tau_critical(k_s_f, E, nu, t_front, b_f_min)
        tau_cr_r = tau_critical(k_s_r, E, nu, t_rear, b_r_min)

        util_f = tau_cr_f / tau_max_front
        util_r = tau_cr_r / tau_max_rear

        results.append({
            "panel": i + 1,
            "bc": bc,
            "a/b_front": ab_f,
            "a/b_rear": ab_r,
            "k_s_front": k_s_f,
            "k_s_rear": k_s_r,
            "tau_max_front": tau_max_front,
            "tau_max_rear": tau_max_rear,
            "tau_cr_front": tau_cr_f,
            "tau_cr_rear": tau_cr_r,
            "util_front": util_f,
            "util_rear": util_r,
            "fails": (util_f < 1.0) or (util_r < 1.0)
        })

        # Plot margin of safety
        y_plot.extend(y_samples)
        MoS_front_plot.extend([util_f - 1] * len(y_samples))
        MoS_rear_plot.extend([util_r - 1] * len(y_samples))

    # Plot
    plt.figure(figsize=(10,5))
    plt.plot(y_plot, MoS_front_plot, label="Front spar MoS")
    plt.plot(y_plot, MoS_rear_plot, label="Rear spar MoS")
    plt.axhline(0, color='k', linestyle='--')
    plt.xlabel("Spanwise position y [m]")
    plt.ylabel("Margin of Safety")
    plt.title("Discretized Margin of Safety along Half-Span")
    plt.legend()
    plt.grid(True)
    plt.show()

    return results

# RUN
if __name__ == "__main__":
    R = compute_spar_buckling(n_ribs)
    for r in R:
        print(f"\nPanel {r['panel']} ({r['bc']})")
        print(f" a/b front = {r['a/b_front']:.3f}, k_s front = {r['k_s_front']:.3f}")
        print(f" a/b rear = {r['a/b_rear']:.3f}, k_s rear = {r['k_s_rear']:.3f}")
        print(f" tau_max front = {r['tau_max_front']:.1f} Pa")
        print(f" tau_max rear = {r['tau_max_rear']:.1f} Pa")
        print(f" tau_cr_front = {r['tau_cr_front']:.1f}, util_front = {r['util_front']:.3f}")
        print(f" tau_cr_rear = {r['tau_cr_rear']:.1f}, util_rear = {r['util_rear']:.3f}")
        if r["fails"]:
            print(" *FAILS: τ_max exceeds critical shear buckling stress*")
        else:
            print(" OK: Panel is safe")
