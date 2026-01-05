import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. IMPORT LOAD FUNCTION
# ==========================================
try:
    from bendingdiagrampositiveload import M_pos_load
except ImportError:
    # Fallback load function (Parabolic approximation)
    print("Warning: 'bendingdiagrampositiveload' not found. Using fallback load function.")
    def M_pos_load(y): return 500000 * (1 - y/11.89)**2

# ==========================================
# 2. SETUP & INPUTS
# ==========================================
E = 72.4e9            # Young's Modulus [Pa] (Al 2024-T3)
sigma_yield = 450e6   # Compressive Yield Strength [Pa]
rho_Al2024 = 2780     # Density [kg/m^3]

half_span = 11.89     # [m]
c_root = 4.02         # [m]
c_tip = 1.27          # [m]
taper = c_tip / c_root

# Normalized Coordinates (Unit Chord c=1)
# 0: Bottom-Left, 1: Bottom-Right, 2: Top-Right, 3: Top-Left
UNIT_CORNERS = [
    (0.2, -0.02723), (0.7, -0.0066),   
    (0.7, 0.0666),   (0.2, 0.08737)
]

# --- DESIGNS DICTIONARY ---
# 'n_top': Number of stringers on the top skin
# 'n_bottom': Number of stringers on the bottom skin
# 'scaling_mode': 'full' (scales width & thick) OR 'width_only' (scales width, const thick)
designs = {
    "Design 1": {
        'n_top': 12, 'n_bottom': 12, 
        'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0015, 't_spar': 0.0015, 
        'scaling_mode': 'full' 
    },
    "Design 2": {
        'n_top': 6, 'n_bottom': 6,
        'w_str': 0.020, 't_str': 0.002, 't_skin': 0.0015, 't_spar': 0.0015, 
        'scaling_mode': 'full'
    },
    "Design 3 (Asymmetric)": {
        'n_top': 14, 'n_bottom': 8,
        'w_str': 0.015, 't_str': 0.001, 't_skin': 0.0030, 't_spar': 0.0030, 
        'scaling_mode': 'full'
    },
    "Design 4": {
        'n_top': 12, 'n_bottom': 12,
        'w_str': 0.020, 't_str': 0.008, 't_skin': 0.0120, 't_spar': 0.0120, 
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
    """Calculates chord length at spanwise location y."""
    return c_root * (1 - (1 - taper) * (y / half_span))

def get_scaled_corners(y):
    """Scales the unit airfoil box to the local chord length."""
    c = get_chord(y)
    return [(pt[0]*c, pt[1]*c) for pt in UNIT_CORNERS]

def get_local_dims(y, params):
    """
    Determines local dimensions (w, t) based on the scaling mode.
    """
    c = get_chord(y)
    mode = params.get('scaling_mode', 'full')
    
    w_base = params['w_str']
    t_str_base = params['t_str']
    t_skin_base = params['t_skin']
    t_spar_base = params.get('t_spar', t_skin_base)
    
    if mode == 'full':
        # Everything scales with chord
        return (w_base * c, t_str_base * c, t_skin_base * c, t_spar_base * c)
    elif mode == 'width_only':
        # Only stringer width scales; thicknesses are constant
        return (w_base * c, t_str_base, t_skin_base, t_spar_base)
    else:
        # Default fallback (Constant everything)
        return (w_base, t_str_base, t_skin_base, t_spar_base)

def calculate_stringer_Ixx_local(w, t):
    """
    Approximates local Ixx of an L-stringer.
    """
    # Vertical Leg
    h1 = w; b1 = t
    A1 = h1 * b1
    y1 = h1 / 2.0
    I1 = (b1 * h1**3) / 12.0

    # Horizontal Leg
    h2 = t; b2 = w - t
    A2 = h2 * b2
    y2 = h2 / 2.0
    I2 = (b2 * h2**3) / 12.0

    # Parallel Axis Theorem for local centroid
    A_total = A1 + A2
    y_c = (A1*y1 + A2*y2) / A_total
    I_local = (I1 + A1*(y1 - y_c)**2) + (I2 + A2*(y2 - y_c)**2)
    
    return I_local

# ==========================================
# 4. CORE CALCULATION FUNCTIONS
# ==========================================

def calculate_centroid_trapezoid(corners, t_skin, n_top, n_bottom, A_str, L_str_dim):
    """
    Calculates the (x, z) centroid of the wing box cross-section.
    
    Args:
        corners: List of (x,z) tuples for box corners.
        t_skin: Skin thickness [m].
        n_top: Number of stringers on top skin.
        n_bottom: Number of stringers on bottom skin.
        A_str: Area of one stringer [m^2].
        L_str_dim: Dimension of stringer (width/height) for offset [m].
        
    Returns:
        (Cx, Cz): Tuple of centroid coordinates (Chordwise, Vertical).
        str_coords: List of (x, z) tuples for all stringers.
    """
    total_area = 0
    moment_x_accumulation = 0  # For finding Cx (Integral of x dA)
    moment_z_accumulation = 0  # For finding Cz (Integral of z dA)

    # --- 1. SKINS & SPARS ---
    num_points = len(corners)
    for i in range(num_points):
        p1 = corners[i]
        p2 = corners[(i + 1) % num_points]

        L_seg = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        
        # Midpoint of the segment
        x_avg = (p1[0] + p2[0]) / 2
        z_avg = (p1[1] + p2[1]) / 2
        
        # Area of segment (Length * Thickness)
        area_seg = L_seg * t_skin 
        
        total_area += area_seg
        moment_x_accumulation += area_seg * x_avg
        moment_z_accumulation += area_seg * z_avg

    # --- 2. STRINGERS ---
    # Top segment: corners[3] -> corners[2]
    # Bot segment: corners[0] -> corners[1]
    segments = [(corners[3], corners[2], "Top"), (corners[0], corners[1], "Bot")]
    str_coords = []
    
    # Offset stringers into the box (approx 25% of stringer height)
    offset_dist = L_str_dim * 0.25 

    for p_start, p_end, side in segments:
        current_n = n_top if side == "Top" else n_bottom
        
        # Distribute stringers evenly along the segment
        for i in range(1, current_n + 1):
            f = i / (current_n + 1)
            sx = p_start[0] + f * (p_end[0] - p_start[0])
            sz = p_start[1] + f * (p_end[1] - p_start[1])

            # Apply vertical offset
            if side == "Top": sz -= offset_dist
            else:             sz += offset_dist
            
            total_area += A_str
            moment_x_accumulation += A_str * sx
            moment_z_accumulation += A_str * sz
            str_coords.append((sx, sz))

    if total_area == 0: return (0, 0), []
    
    Cx = moment_x_accumulation / total_area
    Cz = moment_z_accumulation / total_area
    
    return (Cx, Cz), str_coords

def calculate_Ixx(y, design_params):
    """
    Calculates Area Moment of Inertia (Ixx) and Centroid coordinates.
    
    Returns:
        Ixx: Area Moment of Inertia about the Neutral Axis [m^4].
        (Cx, Cz): Centroid coordinates relative to the leading edge [m].
    """
    n_top = design_params.get('n_top', design_params.get('n_str', 0))
    n_bottom = design_params.get('n_bottom', design_params.get('n_str', 0))
    
    w_str, t_str, t_skin, t_spar = get_local_dims(y, design_params)
    
    # Calculate Stringer Area
    A_str = (w_str * t_str * 2) - (t_str**2)

    corners = get_scaled_corners(y)
    
    # --- 1. GET CENTROID ---
    (Cx, Cz), str_coords = calculate_centroid_trapezoid(corners, t_skin, n_top, n_bottom, A_str, w_str)
    
    Ixx_total = 0
    
    # --- 2. CALCULATE INERTIA (Parallel Axis Theorem) ---
    
    # A. Skins & Spars
    num_points = len(corners)
    for i in range(num_points):
        p1 = corners[i]
        p2 = corners[(i + 1) % num_points]
        
        L_seg = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        dz = p2[1] - p1[1]
        z_avg = (p1[1] + p2[1]) / 2
        
        # Check if segment is a Spar (Indices 1 and 3 are vertical spars)
        t_curr = t_spar if (i == 1 or i == 3) else t_skin
        
        area = L_seg * t_curr
        
        # Local I of inclined thin rectangle: (t * L^3 / 12) * sin^2(theta)
        # sin(theta) = dz / L
        I_local = (t_curr * L_seg**3 / 12.0) * ((dz / L_seg)**2)
        
        # Parallel Axis Term: Area * distance^2
        dist_sq = (z_avg - Cz)**2
        
        Ixx_total += I_local + (area * dist_sq)

    # B. Stringers
    I_str_local = calculate_stringer_Ixx_local(w_str, t_str)
    for _, sz in str_coords:
        dist_sq = (sz - Cz)**2
        Ixx_total += I_str_local + (A_str * dist_sq)
        
    return Ixx_total, (Cx, Cz)

def compressive_strength_only(y_locations, moment_function, design_params):
    """
    Computes the Margin of Safety (or Safety Factor) for compressive failure.
    Uses yield strength of material vs max compressive stress.
    """
    min_mos_per_station = []
    
    for y in y_locations:
        corners = get_scaled_corners(y)

        # Retrieve Ixx and Centroid Z
        I_xx, (Cx, Cz) = calculate_Ixx_and_centroid(y, design_params)
        
        M = abs(moment_function(y))
        
        # Check Stress at Top Skin (Compression in Positive Load Case)
        # We need the maximum distance from the Neutral Axis (Cz) upwards.
        z_top_rear = corners[2][1]
        z_top_front = corners[3][1]
        
        dist_top = max(z_top_rear, z_top_front) - Cz
        
        if I_xx == 0:
            sigma_compressive = 0
        else:
            sigma_compressive = (M * dist_top) / I_xx
        
        # Calculate Safety Factor (Yield / Stress)
        if sigma_compressive > 1e-6:
            sf = sigma_yield / sigma_compressive
        else:
            sf = 100.0  # Infinite safety if no stress
            
        min_mos_per_station.append(sf)
        
    return {
        'y': np.array(y_locations),
        'min_mos': np.array(min_mos_per_station)
    }

# ==========================================
# 5. EXECUTION & PLOTTING
# ==========================================
if __name__ == "__main__":
    y_plot_vals = np.linspace(0, half_span, 200)

    plt.figure(figsize=(10, 6))

    for name, params in designs.items():
        res = compressive_strength_only(y_plot_vals, M_pos_load, params)
        plt.plot(res['y'], res['min_mos'], label=name)
        
        idx_worst = np.argmin(res['min_mos'])
        print(f"[{name}] Min Safety Factor: {res['min_mos'][idx_worst]:.2f} "
              f"at y={res['y'][idx_worst]:.2f} m")

    plt.axhline(1.0, color='r', linestyle='--', label='Failure Threshold (SF = 1.0)')
    plt.ylim(0, 10) 
    plt.xlabel('Distance from Wing Root [m]')
    plt.ylabel('Safety Factor (Yield Strength / Applied Stress)')
    plt.title('Compressive Strength Validation (Positive Load Case)')
    plt.legend()
    plt.grid(True)
    plt.show()