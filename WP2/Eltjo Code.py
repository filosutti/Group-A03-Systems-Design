import numpy as np
from scipy.integrate import quad

# ------------------- Constants -------------------
b = 25.29
C_r = 4.27
lambda_w = 0.32
C_t = 1.35

c_l_alpha = 5.6 # TBD
c_d0 = 0.2      # TBD
tau = 0.5       # fixed
V=228.31
P_req = np.radians(4)          # target roll rate 4°/s converted to rad/s
P_req_safety = 1.5 * P_req    # apply safety factor

# ------------------- Functions -------------------
def c(y):
    return C_r - (2*(C_r-C_t))/b * y

def S_ref(b1, b2):
    return quad(c, b1, b2)[0]

def C_L_delta_a(c_l_alpha, tau, S_reference, b, C_r, b1, b2, lambda_w):
    term1 = 0.5 * (b2*2 - b1*2)
    term2 = (2 * (1 - lambda_w) / (3 * b)) * (b2*3 - b1*3)
    return (2 * c_l_alpha * tau / (S_reference * b)) * C_r * (term1 - term2)

def C_l_p(c_l_alpha, c_d0, S_reference, b, C_r, lambda_w):
    term1 = (1/3) * (b/2)**3
    term2 = ((1 - lambda_w)/(2 * b)) * (b/2)**4
    return -4 * (c_l_alpha + c_d0) / (S_reference * b**2) * C_r * (term1 - term2)

def roll_rate(C_L_delta_a_val, C_l_p_val, delta_a_val, V, b):
    return -C_L_delta_a_val / C_l_p_val * delta_a_val * (2 * V / b)

# ------------------- Iteration -------------------
closest_above = (None, float('inf'))  # (params, excess)

b1_range = np.arange(0.0, 8.0, 0.1)          # m
b2_range = np.arange(0, 11, 0.1)        # m
delta_range = np.radians(np.arange(15, 41, 5))  # 5° to 40°

for b1 in b1_range:
    for b2 in b2_range:
        if b2 <= b1:
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
    print(f"b1={b1:.2f} m, b2={b2:.2f} m, delta_a={da:.1f}°")
    
    # Calculate and show the actual achieved roll rate
    S_reference = S_ref(b1, b2)
    C_lp_val = C_l_p(c_l_alpha, c_d0, S_reference, b, C_r, lambda_w)
    C_L_da = C_L_delta_a(c_l_alpha, tau, S_reference, b, C_r, b1, b2, lambda_w)
    P_actual = roll_rate(C_L_da, C_lp_val, np.radians(da), V, b)
    print(f"Achieved roll rate: {np.degrees(P_actual):.1f}°/s")
else:
    print("No combinations found where P ≥ 1.5 × P_req.")