import numpy as np

# === Constants ===
b = 31.4             # wing span [m]
c_r = 5.015          # root chord [m]
lambda_ = 0.18       # taper ratio
c_l_alpha = 6.436    # lift curve slope [1/rad]
c_d0 = 0.00623       # zero-lift drag coefficient
tau = 0.35           # aileron effectiveness
V = 201              # velocity [m/s]
P_req = 0.56         # required roll rate [rad/s]

# === Functions ===
def S_ref(b1, b2):
    return c_r * (b2 - b1) - 0.13095 * (b2**2 - b1**2)

def C_L_delta_a(b1, b2):
    term = 0.5*(b2**2 - b1**2) - (2*(1 - lambda_)/(3*b))*(b2**3 - b1**3)
    return (2 * c_l_alpha * tau / (S_ref(b1, b2) * b)) * c_r * term

def C_lp(b1, b2):
    term = (1/3)*(b/2)**3 - ((1 - lambda_)/(2*b))*(b/2)**4
    return -4 * (c_l_alpha + c_d0) / (S_ref(b1, b2) * b**2) * c_r * term

def roll_rate(b1, b2, delta_a):
    clp = C_lp(b1, b2)
    if clp != 0:
        return - (C_L_delta_a(b1, b2) / clp) * delta_a * (2 * V / b)
    else:
        return 0

# === Iteration ranges ===
start = 0.75 * (b / 2)
end = b / 2
step = 0.1
b1_values = np.arange(start, end + step, step)
b2_values = np.arange(start, end + step, step)

# delta_a in degrees → radians
delta_a_deg_values = np.arange(10, 18, 1)  # 10° to 17°
delta_a_rad_values = np.radians(delta_a_deg_values)

solutions = []
best_error = float('inf')
best_pair = None

for delta_a, delta_a_deg in zip(delta_a_rad_values, delta_a_deg_values):
    for b1 in b1_values:
        for b2 in b2_values:
            if b2 > b1:
                P = roll_rate(b1, b2, delta_a)
                err = abs(P - P_req)
                if err < 0.01:
                    solutions.append((b1, b2, delta_a_deg, P))
                if err < best_error:
                    best_error = err
                    best_pair = (b1, b2, delta_a_deg, P)

# === Output ===
if solutions:
    print("Possible aileron spans (b1, b2) and deflections achieving required roll rate:")
    for sol in solutions:
        print(f"b1 = {sol[0]:.2f} m, b2 = {sol[1]:.2f} m, δa = {sol[2]:.1f}°, P = {sol[3]:.3f} rad/s")
else:
    print("No exact solution found within tolerance.")
    if best_pair:
        print("\nClosest match:")
        print(f"b1 = {best_pair[0]:.2f} m, b2 = {best_pair[1]:.2f} m, "
              f"δa = {best_pair[2]:.1f}°, P = {best_pair[3]:.3f} rad/s "
              f"(error = {abs(best_pair[3] - P_req):.3f})")
