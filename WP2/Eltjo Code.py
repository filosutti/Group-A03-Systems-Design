import numpy as np
from scipy.integrate import quad

# ------------------- Constants -------------------
b = 25.29       # wingspan [m]
C_r = 4.27      # root chord [m]
lambda_w = 0.32 # taper ratio
C_t = 1.35      # tip chord [m]

c_l_alpha = 5.6 # lift-curve slope [1/rad] (TBD)
c_d0 = 0.2      # drag coefficient increment (TBD)
tau = 0.5       # control effectiveness factor
V = 228.31      # cruise speed TAS [m/s]

P_req = np.radians(10)        # target roll rate (4°/s converted to rad/s)
P_req_safety = 1.5 * P_req   # apply safety factor

# ------------------- Functions -------------------
def c(y):
    """Chord distribution along the semispan."""
    return C_r - (2*(C_r - C_t))/b * y

def S_ref(b1, b2):
    """Reference aileron area (both wings)."""
    return 2 * quad(c, b1, b2)[0]

def C_L_delta_a(c_l_alpha, tau, S_reference, b, C_r, b1, b2, lambda_w):
    """Rolling moment due to aileron deflection."""
    term1 = 0.5 * (b2**2 - b1**2)
    term2 = (2 * (1 - lambda_w) / (3 * b)) * (b2**3 - b1**3)
    return (2 * c_l_alpha * tau / (S_reference * b)) * C_r * (term1 - term2)

def C_l_p(c_l_alpha, c_d0, S_reference, b, C_r, lambda_w):
    """Roll damping derivative."""
    term1 = (1/3) * (b/2)**3
    term2 = ((1 - lambda_w)/(2 * b)) * (b/2)**4
    return -4 * (c_l_alpha + c_d0) / (S_reference * b**2) * C_r * (term1 - term2)

def roll_rate(C_L_delta_a_val, C_l_p_val, delta_a_val, V, b):
    """Achieved roll rate [rad/s]."""
    return -C_L_delta_a_val / C_l_p_val * delta_a_val * (2 * V / b)

# ------------------- Iteration -------------------
closest_above = (None, float('inf'))  # (params, excess)

b1_range = np.arange(5, 8.0, 0.1)          # inner limit [m]
b2_range = np.arange(0.0, b/2, 0.1)          # outer limit [m], capped at semispan
delta_range = np.radians(np.arange(10, 41, 5))  # aileron deflection range [rad]

for b1 in b1_range:
    for b2 in b2_range:
        if b2 <= b1:
            continue
        if (b2 - b1) < 1.5:  # enforce minimum aileron span length
            continue

        S_reference = S_ref(b1, b2)
        C_lp_val = C_l_p(c_l_alpha, c_d0, S_reference, b, C_r, lambda_w)
        for delta_a in delta_range:
            C_L_da = C_L_delta_a(c_l_alpha, tau, S_reference, b, C_r, b1, b2, lambda_w)
            P = roll_rate(C_L_da, C_lp_val, delta_a, V, b)
            if P >= P_req_safety:
                excess = P - P_req_safety
                if excess < closest_above[1]:
                    closest_above = ((b1, b2, np.degrees(delta_a)), excess)

# ------------------- Output -------------------
if closest_above[0]:
    b1, b2, da = closest_above[0]
    print(f"Target roll rate: {np.degrees(P_req):.1f}°/s")
    print(f"Safety factor roll rate (1.5×): {np.degrees(P_req_safety):.1f}°/s")
    print(f"\nBest match (≥ 1.5×P_req):")
    print(f"b1 = {b1:.2f} m, b2 = {b2:.2f} m, span = {b2-b1:.2f} m, delta_a = {da:.1f}°")

    # Calculate and show the actual achieved roll rate
    S_reference = S_ref(b1, b2)
    C_lp_val = C_l_p(c_l_alpha, c_d0, S_reference, b, C_r, lambda_w)
    C_L_da = C_L_delta_a(c_l_alpha, tau, S_reference, b, C_r, b1, b2, lambda_w)
    P_actual = roll_rate(C_L_da, C_lp_val, np.radians(da), V, b)
    print(f"Achieved roll rate: {np.degrees(P_actual):.1f}°/s")
else:
    print("No combinations found where P ≥ 1.5 × P_req.")
