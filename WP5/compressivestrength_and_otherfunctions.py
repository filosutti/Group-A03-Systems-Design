import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. SETUP & INPUTS
# ==========================================
E = 72.4e9            # Young's Modulus [Pa]
sigma_yield = 450e6   # Compressive Yield Strength [Pa]

# Wing Geometry
half_span = 11.89
c_root = 4.02
c_tip = 1.27
taper = c_tip / c_root
loc_front = 0.20
loc_rear = 0.70

# Designs (WP4)
designs = {
    "Design 1": {'n_str': 12, 'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0015, 't_spar': 0.0015},
    "Design 2": {'n_str': 6,  'w_str': 0.020, 't_str': 0.002, 't_skin': 0.0015, 't_spar': 0.0015},
    "Design 3": {'n_str': 6,  'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0030, 't_spar': 0.0030}
}

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

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
    A_str_single = w_str * t_str 
    A_str_total = 2 * n_str * A_str_single 
    I_str = A_str_total * (h_box / 2.0)**2
    
    return I_skin + I_spar + I_str

def compressive_strength_only(y_locations, moment_function, design_params):
    """
    Calculates margins using a Moment Function M(y).
    """
    min_mos_per_station = []
    
    for y in y_locations:
        b_box, h_box = get_box_dims(y)
        I_xx = calculate_Ixx(y, design_params)
        
        # --- CALL YOUR FUNCTION HERE ---
        M = moment_function(y) # Get the moment at exact y
        
        # --- DETERMINE CRITICAL SIDE ---
        if M >= 0:
            z_check = h_box / 2.0  # Top is Compression
        else:
            z_check = -h_box / 2.0 # Bottom is Compression
            
        # --- STRESS CALCULATION ---
        # Bending Stress at critical skin
        sigma_b_skin = -(M * z_check) / I_xx
        
        # Assuming Stringer and Spar Top Edge see same stress as skin
        sigma_critical = sigma_b_skin
        
        # --- MARGIN OF SAFETY ---
        # If stress is Tensile (Positive), margin is infinite for Compressive Failure check
        if sigma_critical >= 0: 
            ms = 100.0
        else:
            # Margin = Yield / abs(Compressive Stress)
            ms = sigma_yield / abs(sigma_critical)
        
        min_mos_per_station.append(ms)
        
    return {
        'y': np.array(y_locations),
        'min_mos': np.array(min_mos_per_station)
    }
# ==========================================
# 3. PLOTTING (Using Imported Positive Load)
# ==========================================
y_plot_vals = np.linspace(0, half_span, 200)

plt.figure(figsize=(10, 6))

for name, params in designs.items():
    # JUST PASS THE IMPORTED FUNCTION HERE 👇
    res = compressive_strength_only(y_plot_vals, M_pos_load, params)
    
    plt.plot(res['y'], res['min_mos'], label=name)
    
    # Print critical margin
    idx_worst = np.argmin(res['min_mos'])
    print(f"{name} Critical MoS: {res['min_mos'][idx_worst]:.2f}")

plt.axhline(1.0, color='r', linestyle='--', label='Failure Threshold')
plt.ylim(0, 5)
plt.xlabel('Span [m]')
plt.ylabel('Margin of Safety')
plt.title('Compressive Strength (Yield) - Positive Load Case')
plt.legend()
plt.grid(True)
plt.show()