import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. IMPORT LOAD FUNCTION
# ==========================================
# This imports the M_pos_load function from your existing file.
# Ensure 'bendingdiagrampositiveload.py' is in the same directory.
from WP4WP5.bendingdiagrampositiveload import M_pos_load

# ==========================================
# 2. SETUP & INPUTS
# ==========================================
# Material Properties: Al2024-T81
E = 72.4e9            # Young's Modulus [Pa]
sigma_yield = 450e6   # Compressive Yield Strength [Pa]

# Wing Geometry
half_span = 11.89     # [m]
c_root = 4.02         # [m]
c_tip = 1.27          # [m]
taper = c_tip / c_root
loc_front = 0.20
loc_rear = 0.70

# Designs (from WP4 Report)
designs = {
    "Design 1": {'n_str': 12, 'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0015, 't_spar': 0.0015},
    "Design 2": {'n_str': 6,  'w_str': 0.020, 't_str': 0.002, 't_skin': 0.0015, 't_spar': 0.0015},
    "Design 3": {'n_str': 6,  'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0030, 't_spar': 0.0030}
}

# ==========================================
# 3. HELPER FUNCTIONS
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
    # Using Flat Bar assumption (w*t)
    A_str_single = w_str * t_str 
    A_str_total = 2 * n_str * A_str_single 
    I_str = A_str_total * (h_box / 2.0)**2
    
    return I_skin + I_spar + I_str

def compressive_strength_only(y_locations, moment_function, design_params):
    """
    Calculates margins for components based on Positive Moment (Top Compression).
    """
    skin_mos = []
    spar_mos = []
    str_mos = []
    min_mos_per_station = []
    
    for y in y_locations:
        b_box, h_box = get_box_dims(y)
        I_xx = calculate_Ixx(y, design_params)
        
        # Load from imported function
        M = abs(moment_function(y)) # Magnitude of positive moment
        
        # --- STRESS CALCULATION ---
        # For Positive Load, Top Skin is in Compression.
        # Max distance from neutral axis z = h/2
        z_max = h_box / 2.0
        
        # Calculate compressive stress magnitude
        sigma_compressive = (M * z_max) / I_xx
        
        # --- MARGIN OF SAFETY ---
        # MS = Yield Stress / Applied Stress
        # 1. Skin (Top)
        ms_skin = sigma_yield / sigma_compressive if sigma_compressive > 1e-6 else 100.0
        skin_mos.append(ms_skin)
        
        # 2. Stringer (Top - Attached to Skin)
        # Experiences same stress as skin
        str_mos.append(ms_skin)
        
        # 3. Spar (Top Edge)
        # Checking spar web at the top edge (same stress as skin)
        spar_mos.append(ms_skin)
        
        # Minimum margin
        min_mos_per_station.append(ms_skin)
        
    return {
        'y': np.array(y_locations),
        'min_mos': np.array(min_mos_per_station)
    }

# ==========================================
# 4. PLOTTING
# ==========================================
# Resolution for the plot
y_plot_vals = np.linspace(0, half_span, 200)

plt.figure(figsize=(10, 6))

for name, params in designs.items():
    # Pass the imported M_pos_load function directly
    res = compressive_strength_only(y_plot_vals, M_pos_load, params)
    
    plt.plot(res['y'], res['min_mos'], label=name)
    
    # Print critical margin
    idx_worst = np.argmin(res['min_mos'])
    print(f"{name} Critical MoS: {res['min_mos'][idx_worst]:.2f} at y={res['y'][idx_worst]:.2f}m")

plt.axhline(1.0, color='r', linestyle='--', label='Failure Threshold')
plt.ylim(0, 5) # Zoom in on the critical range
plt.xlabel('Span [m]')
plt.ylabel('Margin of Safety')
plt.title('Compressive Strength (Yield) - Positive Load Case')
plt.legend()
plt.grid(True)
plt.show()