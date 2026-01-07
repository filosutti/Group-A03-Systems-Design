import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. IMPORT LOAD FUNCTION
# ==========================================
try:
    from bendingdiagrampositiveload import M_pos_load
except ImportError:
    # Fallback load function if file not found
    def M_pos_load(y): return 500000 * (1 - y/11.89)**2

# ==========================================
# 2. SETUP & INPUTS
# ==========================================
E = 72.4e9            # Young's Modulus [Pa]
sigma_yield = 450e6   # Compressive Yield Strength [Pa]
rho_Al2024 = 2780     # Density [kg/m^3]

half_span = 11.89     # [m]
c_root = 4.02         # [m]
c_tip = 1.27          # [m]
taper = c_tip / c_root

# Normalized Coordinates (Unit Chord c=1)
UNIT_CORNERS = [
    (0.2, -0.02723), (0.7, -0.0066),   
    (0.7, 0.0666),   (0.2, 0.08737)
]

# --- DESIGNS DICTIONARY ---
designs = {
    "1 min tens": {
        'n_top': 3, 'n_bottom': 12,
        'w_str': 0.015, 't_str': 0.004, 't_skin': 0.006, 't_spar': 0.006,
        'scaling_mode': 'width_only'
    },
    "2 min tens": {
        'n_top': 1, 'n_bottom': 6,
        'w_str': 0.020, 't_str': 0.008, 't_skin': 0.006, 't_spar': 0.006,
        'scaling_mode': 'width_only'
    },
    "3 min tens": {
        'n_top': 0, 'n_bottom': 6,
        'w_str': 0.015, 't_str': 0.004, 't_skin': 0.012, 't_spar': 0.012,
        'scaling_mode': 'width_only'
    },
    "1 min comp": {
        'n_top': 12, 'n_bottom': 1,
        'w_str': 0.015, 't_str': 0.004, 't_skin': 0.006, 't_spar': 0.006,
        'scaling_mode': 'width_only'
    },
    "2 min comp": {
        'n_top': 6, 'n_bottom': 0,
        'w_str': 0.020, 't_str': 0.008, 't_skin': 0.006, 't_spar': 0.006,
        'scaling_mode': 'width_only'
    },
    "3 min comp": {
        'n_top': 6, 'n_bottom': 0,
        'w_str': 0.015, 't_str': 0.004, 't_skin': 0.012, 't_spar': 0.012,
        'scaling_mode': 'width_only'
    },
    "Image Design 1": {
        'n_top': 12, 'n_bottom': 12,
        'w_str': 0.015, 't_str': 0.004, 't_skin': 0.006, 't_spar': 0.006,
        'scaling_mode': 'width_only'
    },
    "Image Design 2": {
        'n_top': 6, 'n_bottom': 6,
        'w_str': 0.020, 't_str': 0.008, 't_skin': 0.006, 't_spar': 0.006,
        'scaling_mode': 'width_only'
    },
    "Image Design 3": {
        'n_top': 6, 'n_bottom': 6,
        'w_str': 0.015, 't_str': 0.004, 't_skin': 0.012, 't_spar': 0.012,
        'scaling_mode': 'width_only'
    }
}

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def get_chord(y):
    return c_root * (1 - (1 - taper) * (y / half_span))

def get_scaled_corners(y):
    c = get_chord(y)
    return [(pt[0]*c, pt[1]*c) for pt in UNIT_CORNERS]

def get_local_dims(y, params):
    """
    Determines local dimensions (w, t) based on the scaling mode.
    """
    c = get_chord(y)
    mode = params.get('scaling_mode', 'full')
    
    # Base values from dictionary
    w_base = params['w_str']
    t_str_base = params['t_str']
    t_skin_base = params['t_skin']
    t_spar_base = params.get('t_spar', t_skin_base)
    
    if mode == 'full':
        w_str = w_base * c
        t_str = t_str_base * c
        t_skin = t_skin_base * c
        t_spar = t_spar_base * c
    elif mode == 'width_only':
        w_str = w_base * c
        t_str = t_str_base
        t_skin = t_skin_base
        t_spar = t_spar_base
    else:
        w_str = w_base
        t_str = t_str_base
        t_skin = t_skin_base
        t_spar = t_spar_base

    return w_str, t_str, t_skin, t_spar

def calculate_centroid_trapezoid(corners, t_skin, n_top, n_bottom, A_str, L_str_dim):
    total_mass = 0
    moment_z = 0 

    # --- 1. SKINS (and Spars) ---
    num_points = len(corners)
    for i in range(num_points):
        p1 = corners[i]
        p2 = corners[(i + 1) % num_points]

        L_seg = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        z_avg = (p1[1] + p2[1]) / 2
        
        m_seg = L_seg * t_skin * rho_Al2024
        total_mass += m_seg
        moment_z += m_seg * z_avg

    # --- 2. STRINGERS ---
    # Top segment is corners[3] -> corners[2]
    # Bottom segment is corners[0] -> corners[1]
    segments = [(corners[3], corners[2], "Top"), (corners[0], corners[1], "Bot")]
    str_coords = []
    
    offset_dist = L_str_dim * 0.25 

    for p_start, p_end, side in segments:
        # SELECT correct number of stringers based on side
        current_n = n_top if side == "Top" else n_bottom
        
        for i in range(1, current_n + 1):
            f = i / (current_n + 1)
            sx = p_start[0] + f * (p_end[0] - p_start[0])
            sz = p_start[1] + f * (p_end[1] - p_start[1])

            if side == "Top": sz -= offset_dist
            else:             sz += offset_dist
            
            m_str = A_str * rho_Al2024
            total_mass += m_str
            moment_z += m_str * sz
            str_coords.append((sx, sz))

    if total_mass == 0: return 0, []
    
    Cy = moment_z / total_mass
    return Cy, str_coords

def calculate_stringer_Ixx_local(w, t):
    # L-stringer local inertia approximation
    h1 = w; b1 = t
    A1 = h1 * b1
    y1 = h1 / 2.0
    I1 = (b1 * h1**3) / 12.0

    h2 = t; b2 = w - t
    A2 = h2 * b2
    y2 = h2 / 2.0
    I2 = (b2 * h2**3) / 12.0

    A_total = A1 + A2
    y_c = (A1*y1 + A2*y2) / A_total
    I_local = (I1 + A1*(y1 - y_c)**2) + (I2 + A2*(y2 - y_c)**2)
    
    return I_local

def calculate_Ixx(y, design_params):
    n_top = design_params.get('n_top', design_params.get('n_str', 0))
    n_bottom = design_params.get('n_bottom', design_params.get('n_str', 0))
    
    w_str, t_str, t_skin, t_spar = get_local_dims(y, design_params)
    
    # Calculate Stringer Area
    A_str = (w_str * t_str * 2) - (t_str**2)

    corners = get_scaled_corners(y)
    
    # Pass n_top and n_bottom to centroid function
    Cy, str_coords = calculate_centroid_trapezoid(corners, t_skin, n_top, n_bottom, A_str, w_str)
    
    Ixx_total = 0
    
    # Skins & Spars
    num_points = len(corners)
    for i in range(num_points):
        p1 = corners[i]
        p2 = corners[(i + 1) % num_points]
        
        L_seg = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        dz = p2[1] - p1[1]
        z_avg = (p1[1] + p2[1]) / 2
        
        t_curr = t_spar if (i == 1 or i == 3) else t_skin
        
        area = L_seg * t_curr
        I_local = (t_curr * (L_seg**3) * ((dz/L_seg)**2)) / 12.0
        dist_sq = (z_avg - Cy)**2
        Ixx_total += I_local + (area * dist_sq)

    # Stringers (str_coords already contains correct number of points from centroid func)
    I_str_local = calculate_stringer_Ixx_local(w_str, t_str)
    for _, sz in str_coords:
        dist_sq = (sz - Cy)**2
        Ixx_total += I_str_local + (A_str * dist_sq)
        
    return Ixx_total

def compressive_strength_only(y_locations, moment_function, design_params):
    min_mos_per_station = []
    
    for y in y_locations:
        # Extract params
        n_top = design_params.get('n_top', design_params.get('n_str', 0))
        n_bottom = design_params.get('n_bottom', design_params.get('n_str', 0))

        corners = get_scaled_corners(y)
        w_str, t_str, t_skin, t_spar = get_local_dims(y, design_params)
        A_str = (w_str * t_str * 2) - (t_str**2)
        
        # Calculate properties
        Cy, _ = calculate_centroid_trapezoid(corners, t_skin, n_top, n_bottom, A_str, w_str)
        I_xx = calculate_Ixx(y, design_params)
        M = abs(moment_function(y))
        
        # Check Stress at Top Skin (Compression in Positive Load Case)
        z_top_rear = corners[2][1]
        z_top_front = corners[3][1]
        # Max distance from neutral axis to top skin
        dist_top = max(z_top_rear, z_top_front) - Cy
        
        if I_xx == 0:
            sigma_compressive = 0
        else:
            sigma_compressive = (M * dist_top) / I_xx
        
        if sigma_compressive > 1e-6:
            sf = sigma_yield / sigma_compressive
        else:
            sf = 100.0
            
        min_mos_per_station.append(sf)
        
    return {
        'y': np.array(y_locations),
        'min_mos': np.array(min_mos_per_station)
    }

# ==========================================
# 4. PLOTTING
# ==========================================
y_plot_vals = np.linspace(0, half_span, 200)

plt.figure(figsize=(10, 6))

for name, params in designs.items():
    res = compressive_strength_only(y_plot_vals, M_pos_load, params)
    plt.plot(res['y'], res['min_mos'], label=name)
    
    idx_worst = np.argmin(res['min_mos'])
    print(f"{name} Min Safety Factor: {res['min_mos'][idx_worst]:.2f} at y={res['y'][idx_worst]:.2f}m")

plt.axhline(1.0, color='r', linestyle='--', label='Failure Threshold (SF = 1.0)')
plt.ylim(0, 10) 
plt.xlabel('Distance from Wing Root [m]')
plt.ylabel('Safety Factor (Yield Strength / Applied Stress)')
plt.title('Compressive Strength Validation (Positive Load Case)')
plt.legend()
plt.grid(True)
plt.show()