import numpy as np
import matplotlib.pyplot as plt

# ==============
# SETUP & INPUTS
# ==============
# Material Properties: Al2024-T81
E = 72.4e9            # Young's Modulus [Pa]
nu = 0.33             # Poisson's ratio
sigma_yield = 450e6   # Compressive Yield Strength [Pa]

# Wing Geometry
half_span = 11.89     # [m]
c_root = 4.02         # [m]
c_tip = 1.27          # [m]
taper = c_tip / c_root
loc_front = 0.20
loc_rear = 0.70

# Designs (WP4)
designs = {
    "Design 1": {'n_str': 12, 'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0015, 't_spar': 0.0015},
    "Design 2": {'n_str': 6,  'w_str': 0.020, 't_str': 0.002, 't_skin': 0.0015, 't_spar': 0.0015},
    "Design 3": {'n_str': 6,  'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0030, 't_spar': 0.0030}
}

# =========
# FUNCTIONS
# =========

def get_chord(y):
    return c_root * (1 - (1 - taper) * (y / half_span))

def get_box_dims(y):
    c = get_chord(y)
    b_box = c * (loc_rear - loc_front)
    h_box = c * 0.12 * 0.9 
    return b_box, h_box

def calculate_Ixx(y, design_params):
    """Calculates Ixx using the FULL cross-section (Top + Bottom)."""
    b_box, h_box = get_box_dims(y)
    n_str = design_params['n_str']
    t_skin = design_params['t_skin']
    t_spar = design_params['t_spar']
    w_str = design_params['w_str']
    t_str = design_params['t_str']
    
    # 1. Skin (Top + Bottom)
    A_skin_flange = b_box * t_skin
    I_skin = 2 * (A_skin_flange * (h_box / 2)**2)
    
    # 2. Spar Webs (Vertical)
    I_spar = 2 * (t_spar * h_box**3 / 12.0)
    
    # 3. Stringers (Top + Bottom)
    # Using Flat Bar assumption (w*t) as per previous feedback
    A_str_single = w_str * t_str 
    A_str_total = 2 * n_str * A_str_single 
    I_str = A_str_total * (h_box / 2.0)**2
    
    return I_skin + I_spar + I_str

def compressive_strength_only(y_locations, M_distribution, design_params, N_distribution=None):
    """
    Calculates margins for components based on signed Moment.
    - Checks Top components if M > 0 (Compression on Top)
    - Checks Bottom components if M < 0 (Compression on Bottom)
    """
    if N_distribution is None:
        N_distribution = np.zeros_like(M_distribution)
    
    skin_mos = []
    spar_mos = []
    str_mos = []
    min_mos_per_station = []
    
    for i, y in enumerate(y_locations):
        b_box, h_box = get_box_dims(y)
        I_xx = calculate_Ixx(y, design_params)
        
        # Dimensions
        t_skin = design_params['t_skin']
        t_spar = design_params['t_spar']
        n_str = design_params['n_str']
        w_str = design_params['w_str']
        t_str = design_params['t_str']
        
        # Areas for Axial Stress
        A_str_single = w_str * t_str
        A_skin_total = 2 * b_box * t_skin
        A_spar_total = 2 * t_spar * h_box
        A_str_total = 2 * n_str * A_str_single
        A_section = A_skin_total + A_spar_total + A_str_total
        
        # Loads
        M = M_distribution[i] # KEEP SIGN
        N = N_distribution[i] # KEEP SIGN (assume + is tension)
        
        # Axial Stress (Uniform) - Negative N increases compression
        # Note: If N is tension (+), it reduces compressive stress.
        # We need to check if the combined stress is compressive (negative).
        sigma_axial = N / A_section if A_section > 0 else 0.0
        
        # --- DETERMINE CRITICAL SIDE ---
        # Bending Stress = - (M * z) / I
        # If M > 0 (Smile): Top (z > 0) is Compression (-).
        # If M < 0 (Frown): Bottom (z < 0) is Compression (-).
        
        if M >= 0:
            # Check TOP Side (z = +h/2)
            z_check = h_box / 2.0
        else:
            # Check BOTTOM Side (z = -h/2)
            z_check = -h_box / 2.0
            
        # --- 1. SKIN CHECK ---
        # Bending Stress at critical skin
        # Formula: sigma = - (M * z) / I (Standard beam sign convention)
        sigma_b_skin = -(M * z_check) / I_xx
        sigma_skin_total = sigma_b_skin + sigma_axial
        
        # --- 2. STRINGER CHECK ---
        # Stringers are attached to skin, assume same z
        sigma_str_total = sigma_skin_total
        
        # --- 3. SPAR CHECK ---
        # FIX ISSUE 2: Check spar at same z as skin (top/bottom edge)
        # The spar web extends from -h/2 to +h/2. The max stress is at the edge.
        sigma_spar_total = sigma_skin_total
        
        # --- Margins of Safety ---
        # We only care if the stress is COMPRESSIVE (Negative in standard convention)
        # Margin = Yield / abs(Compressive Stress)
        
        def get_ms(stress_val):
            # If stress is positive (Tension), margin is infinite for Compressive Failure
            if stress_val >= 0: 
                return 100.0
            # If stress is negative (Compression), check magnitude against yield
            return sigma_yield / abs(stress_val)
            
        skin_mos.append(get_ms(sigma_skin_total))
        str_mos.append(get_ms(sigma_str_total))
        spar_mos.append(get_ms(sigma_spar_total))
        
        # Minimum margin
        min_mos_per_station.append(min(skin_mos[-1], str_mos[-1], spar_mos[-1]))
        
    return {
        'y': y_locations,
        'min_mos': np.array(min_mos_per_station)
    }

# ========
# PLOTTING
# ========
y_vals = np.linspace(0, half_span, 100)
# Example Loads (REPLACE WITH YOUR WP4 DATA)
M_dist = 3000000 * (1 - y_vals/half_span)**2 # Positive M -> Top Compression
N_dist = np.zeros_like(M_dist)

plt.figure(figsize=(10, 6))
for name, params in designs.items():
    res = compressive_strength_only(y_vals, M_dist, params, N_dist)
    plt.plot(res['y'], res['min_mos'], label=name)

plt.axhline(1.0, color='r', linestyle='--', label='Failure')
plt.ylim(0, 5)
plt.xlabel('Span [m]')
plt.ylabel('Margin of Safety')
plt.title('Compressive Strength (Yield)')
plt.legend()
plt.grid(True)
plt.show()