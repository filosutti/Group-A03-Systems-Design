import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. IMPORT LOAD FUNCTION
# ==========================================
# Ensure 'bendingdiagrampositiveload.py' is in the same directory.
try:
    from bendingdiagrampositiveload import M_pos_load
except ImportError:
    # Fallback for testing if file not present (Dummy Load)
    def M_pos_load(y): return 500000 * (1 - y/11.89)**2

# ==========================================
# 2. SETUP & INPUTS
# ==========================================
# Material Properties: Al2024-T81
E = 72.4e9            # Young's Modulus [Pa]
sigma_yield = 450e6   # Compressive Yield Strength [Pa]
rho_Al2024 = 2780     # Density [kg/m^3]

# Wing Geometry
half_span = 11.89     # [m]
c_root = 4.02         # [m]
c_tip = 1.27          # [m]
taper = c_tip / c_root

# NORMALIZED CORNER COORDINATES (at Unit Chord c=1)
# Order: Bottom-Front -> Bottom-Rear -> Top-Rear -> Top-Front
UNIT_CORNERS = [
    (0.2, -0.02723), 
    (0.7, -0.0066),   
    (0.7, 0.0666),   
    (0.2, 0.08737)
]

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

def get_scaled_corners(y):
    """
    Scales the normalized unit-chord coordinates to the actual wing chord at span y.
    Returns: list of (x, z) tuples
    """
    c = get_chord(y)
    # Multiply unit coords (x/c, z/c) by actual chord c
    return [(pt[0]*c, pt[1]*c) for pt in UNIT_CORNERS]

def calculate_centroid_trapezoid(corners, t_skin, n_str, A_str, L_str_dim):
    """
    Calculates Cy (neutral axis z-height) using correct mass properties.
    """
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
    # User specified: Top = corners[3]->[2], Bot = corners[0]->[1]
    segments = [
        (corners[3], corners[2], "Top"), 
        (corners[0], corners[1], "Bot")
    ]
    
    str_coords = []
    offset_dist = L_str_dim * 0.25 

    for p_start, p_end, side in segments:
        for i in range(1, n_str + 1):
            f = i / (n_str + 1)
            
            # Position on Skin
            sx = p_start[0] + f * (p_end[0] - p_start[0])
            sz = p_start[1] + f * (p_end[1] - p_start[1])

            # Apply Offset 
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
    """
    Calculates local Ixx of an L-stringer about its own horizontal centroidal axis.
    Assuming Equal-Leg Angle (width = height = w).
    """
    # 1. Define sub-rectangles
    # Vertical Leg: dimensions t (width) x w (height)
    h1 = w; b1 = t
    A1 = h1 * b1
    y1 = h1 / 2.0  # Centroid height from bottom
    I1 = (b1 * h1**3) / 12.0

    # Horizontal Leg: dimensions (w-t) (width) x t (height)
    h2 = t; b2 = w - t
    A2 = h2 * b2
    y2 = h2 / 2.0  # Centroid height from bottom
    I2 = (b2 * h2**3) / 12.0

    # 2. Find Combined Centroid (y_c)
    A_total = A1 + A2
    y_c = (A1*y1 + A2*y2) / A_total

    # 3. Parallel Axis Theorem for Local Ixx
    I_local = (I1 + A1*(y1 - y_c)**2) + (I2 + A2*(y2 - y_c)**2)
    
    return I_local

def calculate_Ixx(y, design_params):
    """
    Calculates Ixx using the scaled Trapezoidal geometry.
    INCLUDES LOCAL INERTIA OF STRINGERS (No point-mass simplification).
    """
    n_str = design_params['n_str']
    t_skin = design_params['t_skin']
    t_spar = design_params.get('t_spar', t_skin)
    
    w_str = design_params['w_str']
    t_str = design_params['t_str']
    
    # Calculate Stringer Area
    A_str = (w_str * t_str * 2) - (t_str**2)

    # 1. Get Scaled Geometry
    corners = get_scaled_corners(y)
    
    # 2. Find Neutral Axis (Centroid)
    Cy, str_coords = calculate_centroid_trapezoid(corners, t_skin, n_str, A_str, w_str)
    
    Ixx_total = 0
    
    # 3. Calculate Ixx - Skin & Spars
    num_points = len(corners)
    for i in range(num_points):
        p1 = corners[i]
        p2 = corners[(i + 1) % num_points]
        
        # Segment Geometry
        L_seg = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        dz = p2[1] - p1[1]
        z_avg = (p1[1] + p2[1]) / 2
        
        # Determine thickness (Spars are indices 1 and 3)
        t_curr = t_spar if (i == 1 or i == 3) else t_skin
        
        area = L_seg * t_curr
        
        # Local Ixx of inclined segment
        I_local = (t_curr * (L_seg**3) * ((dz/L_seg)**2)) / 12.0
        
        # Parallel Axis Theorem
        dist_sq = (z_avg - Cy)**2
        Ixx_total += I_local + (area * dist_sq)

    # 4. Calculate Ixx - Stringers
    # --- UPDATE: Explicitly calculating local Ixx for stringers ---
    I_str_local = calculate_stringer_Ixx_local(w_str, t_str)
    
    for _, sz in str_coords:
        dist_sq = (sz - Cy)**2
        # Sum of Local Inertia + Steiner Term (Ad^2)
        Ixx_total += I_str_local + (A_str * dist_sq)
        
    return Ixx_total

def compressive_strength_only(y_locations, moment_function, design_params):
    """
    Calculates margins using the updated Trapezoidal Ixx logic.
    Maintains original function name and inputs.
    """
    min_mos_per_station = []
    
    for y in y_locations:
        # Re-calculate Geometry locally to get max distance to top skin
        corners = get_scaled_corners(y)
        
        n_str = design_params['n_str']
        w_str = design_params['w_str']
        t_str = design_params['t_str']
        A_str = (w_str * t_str * 2) - (t_str**2)
        
        # Get Centroid z-position (Cy)
        Cy, _ = calculate_centroid_trapezoid(corners, design_params['t_skin'], n_str, A_str, w_str)
        
        # Get Inertia
        I_xx = calculate_Ixx(y, design_params)
        
        M = abs(moment_function(y))
        
        # --- STRESS CALCULATION ---
        # Find max distance from neutral axis (Cy) to the Top Skin (Compression side)
        # Top corners are indices 2 and 3
        z_top_rear = corners[2][1]
        z_top_front = corners[3][1]
        
        # Max distance from neutral axis to the highest point of the structure
        dist_top = max(z_top_rear, z_top_front) - Cy
        
        if I_xx == 0:
            sigma_compressive = 0
        else:
            sigma_compressive = (M * dist_top) / I_xx
        
        # --- MARGIN OF SAFETY ---
        ms = sigma_yield / sigma_compressive if sigma_compressive > 1e-6 else 100.0
        min_mos_per_station.append(ms)
        
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
    res = compressive_strength_only(y_plot_vals, M_pos_load, params)
    
    plt.plot(res['y'], res['min_mos'], label=name)
    
    # Print critical margin
    idx_worst = np.argmin(res['min_mos'])
    print(f"{name} Critical MoS: {res['min_mos'][idx_worst]:.2f} at y={res['y'][idx_worst]:.2f}m")

plt.axhline(1.0, color='r', linestyle='--', label='Failure Threshold')
plt.ylim(0, 5) 
plt.xlabel('Span [m]')
plt.ylabel('Margin of Safety')
plt.title('Compressive Strength (Trapezoidal Wingbox) - Positive Load Case')
plt.legend()
plt.grid(True)
plt.show()