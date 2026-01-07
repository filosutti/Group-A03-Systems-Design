import numpy as np

def wingbox_weight_halfwing(
    N_stringers,
    t_skin,
    t_stringer,
    k,
    rho=2780.0,
    b_half=11.89,
    c_root=4.02,
    c_tip=1.27,
    x_front=0.2,
    x_rear=0.7,
    n_span=1000
):
    """
    All thicknesses in meters.
    k defines stringer leg length: a(y) = k * c(y) [mm]
    """

    # Spanwise grid
    y = np.linspace(0.0, b_half, n_span)

    # Linear chord distribution
    c = c_root + (c_tip - c_root) * (y / b_half)

    # Wingbox width
    w_box = (x_rear - x_front) * c

    # ---- Spar heights from provided coordinates ----
    h_front = c * (0.08737 - (-0.02723))
    h_rear  = c * (0.0666  - (-0.0066))
    h_spar  = 0.5 * (h_front + h_rear)

    # ---- Skins ----
    A_skin = w_box * t_skin
    W_top_skin = rho * np.trapezoid(A_skin, y)
    W_bot_skin = W_top_skin

    # ---- Spars (2) ----
    A_spar = h_spar * t_skin
    W_spars = 2.0 * rho * np.trapezoid(A_spar, y)

    # ---- Stringers ----
    a = (k * c) / 1000.0  # mm → m
    A_str = 2.0 * a * t_stringer - t_stringer**2
    W_stringers = rho * N_stringers * np.trapezoid(A_str, y)

    # ---- Totals ----
    W_total = W_top_skin + W_bot_skin + W_spars + W_stringers

    return {
        "Top skin weight [kg]": float(W_top_skin),
        "Bottom skin weight [kg]": float(W_bot_skin),
        "Spar weight [kg]": float(W_spars),
        "Stringer weight [kg]": float(W_stringers),
        "Total wingbox weight [kg]": float(W_total)
    }

#change values below to compute weight of any wingbox, they are in order: nr of stringers, skin and spar thickness, stringer thickness, stringer width k factor, multyplied by the chord length to get the stringer width
print(wingbox_weight_halfwing(16, 0.006, 0.004, 15))