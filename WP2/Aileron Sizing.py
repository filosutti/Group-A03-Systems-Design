import numpy as np
from scipy.integrate import quad

# ------------------- Constants -------------------
b = 25.29
C_r = 4.27
lambda_w = 0.32
C_t = 1.35

c_l_alpha = 5.73    # 2D lift curve slope [1/rad]
c_d0 = 6*0.0027       # profile drag
tau = 0.21          # control surface effectiveness
P_req = np.radians(4)       # target roll rate [rad/s] (4°/s)
P_req_safety = 5*P_req  # safety factor
b_2outer_limit = 10.5  #outer limit for b2
b_1outer_limit = 8     #outer limit for b1
b_1inner_limit = 5  #inner limit for b1 
b_2iinner_limit = 8.5  #inner limit for b2
delta_a_innerlimit = 8
delta_a_outerlimit = 15

CL_Max=1.52
M_Max=32142
S=70.885
T=288.15
R=287
P=101325
g=9.80665

W_Max=M_Max*g
density=P/(R*T)
V_sr=(2*W_Max/(S*density*CL_Max))*(0.5)
V=1.13*V_sr    #Minimum roll speed according to CS25

# ------------------- Functions -------------------
def c(y):
    """Chord distribution (linear taper)."""
    return C_r - (2*(C_r-C_t))/b * y

def S_ref(b1, b2):
    """Reference aileron area between y=b1 and y=b2."""
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
best_solution = None
smallest_error = float("inf")

# Reasonable search ranges for ailerons
b1_range = np.arange(b_1inner_limit, b_1outer_limit, 0.1)     # inboard start [m]
b2_range = np.arange(b_2iinner_limit, b_2outer_limit, 0.1)    # outboard end [m]
delta_range = np.radians(np.arange(delta_a_innerlimit, delta_a_outerlimit, 1))  # deflection [°]

for b1 in b1_range:
    for b2 in b2_range:
        if b2 <= b1:
            continue
        S_reference = S_ref(b1, b2)
        C_lp_val = C_l_p(c_l_alpha, c_d0, S_reference, b, C_r, lambda_w)
        for delta_a in delta_range:
            C_L_da = C_L_delta_a(c_l_alpha, tau, S_reference, b, C_r, b1, b2, lambda_w)
            P = roll_rate(C_L_da, C_lp_val, delta_a, V, b)

            # Only consider feasible designs (≥ safety requirement)
            if P >= P_req_safety:
                error = abs(P - P_req_safety)
                if error < smallest_error:
                    smallest_error = error
                    best_solution = (b1, b2, np.degrees(delta_a), P)

# ------------------- Output -------------------
if best_solution:
    b1, b2, da, P_actual = best_solution
    print(f"Target roll rate: {np.degrees(P_req):.2f}°/s")
    print(f"Safety factor roll rate (1.5×): {np.degrees(P_req_safety):.2f}°/s")
    print("\nBest match (≥ 1.5×P_req):")
    print(f"  Inboard start b1 = {b1:.2f} m")
    print(f"  Outboard end   b2 = {b2:.2f} m")
    print(f"  Deflection     δa = {da:.1f}°")
    print(f"Achieved roll rate: {np.degrees(P_actual):.2f}°/s")
    print(f"Reference area: {S_reference:.2f} m2")

else:
    print("No feasible aileron configuration found.")