import numpy as np
import matplotlib.pyplot as plt

def calculate_wingbox_centroid(corners, skin_thickness, skin_density, n_str, A_str):
    """
    Calculates centroid including auto-generated stringers.
    Returns: (Cx, Cy, stringer_coordinates_list)
    """
    total_mass = 0
    moment_x = 0
    moment_y = 0

    print(f"{'Component':<15} {'Len/Area':<12} {'Mass (kg)':<12} {'Centroid (x,y)'}")
    print("-" * 65)

    # --- 1. SKINS ---
    num_points = len(corners)
    for i in range(num_points):
        p1 = corners[i]
        p2 = corners[(i + 1) % num_points]

        L = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        xc_seg = (p1[0] + p2[0]) / 2
        yc_seg = (p1[1] + p2[1]) / 2
        m_seg = L * skin_thickness * skin_density

        total_mass += m_seg
        moment_x += m_seg * xc_seg
        moment_y += m_seg * yc_seg

        print(f"Skin {i+1}-{((i+1)%4)+1:<9} {L:<12.4f} {m_seg:<12.4f} ({xc_seg:.3f}, {yc_seg:.3f})")

    print("-" * 65)

    # --- 2. STRINGERS (Generated Internally) ---
    # Define segments: Top (Front-Top->Rear-Top) and Bot (Front-Bot->Rear-Bot)
    # Indices: 0:Front-Bot, 1:Rear-Bot, 2:Rear-Top, 3:Front-Top
    segments = [(corners[3], corners[2]), (corners[0], corners[1])]
    
    stringer_coords = [] # Store coordinates to return for plotting
    count = 1

    for p_start, p_end in segments:
        for i in range(1, n_str + 1):
            f = i / (n_str + 1) # Interpolation fraction
            
            # Position
            sx = p_start[0] + f * (p_end[0] - p_start[0])
            sy = p_start[1] + f * (p_end[1] - p_start[1])
            
            # Mass
            m_str = A_str * skin_density
            
            # Add to Totals
            total_mass += m_str
            moment_x += m_str * sx
            moment_y += m_str * sy
            
            # Store and Print
            stringer_coords.append((sx, sy))
            print(f"Stringer {count:<6} {A_str:<12.6f} {m_str:<12.4f} ({sx:.3f}, {sy:.3f})")
            count += 1

    # --- 3. FINAL CALCULATION ---
    if total_mass == 0: return 0, 0, []

    Cx = moment_x / total_mass
    Cy = moment_y / total_mass

    return Cx, Cy, stringer_coords

# ==========================================
# INPUTS
# ==========================================

# 1. Geometry (Front-Bot -> Rear-Bot -> Rear-Top -> Front-Top)
coords = [
    (0.2, -0.02723),  
    (0.7, -0.0066),   
    (0.7, 0.0666),    
    (0.2, 0.08737)    
]

# 2. Material & Stringer Params
t_skin = 0.001          # Skin thickness (m)
rho_Al2024 = 2780       # Density (kg/m^3)
n_stringers_side = 10   # Stringers per side
A_stringer = 0.0023     # Area per stringer (m^2)

# ==========================================
# EXECUTION
# ==========================================

cx, cy, str_coords = calculate_wingbox_centroid(coords, t_skin, rho_Al2024, n_stringers_side, A_stringer)

print("="*30)
print(f"FINAL CENTROID: ({cx:.5f}, {cy:.5f})")
print("="*30)

# ==========================================
# VISUALIZATION
# ==========================================
x_box = [p[0] for p in coords] + [coords[0][0]]
y_box = [p[1] for p in coords] + [coords[0][1]]

plt.figure(figsize=(10, 6))
plt.plot(x_box, y_box, 'b-', label='Skin', linewidth=2)
plt.fill(x_box, y_box, alpha=0.1)

# Plot Stringers (using the list returned by the function)
if str_coords:
    sx_list, sy_list = zip(*str_coords)
    plt.scatter(sx_list, sy_list, color='red', s=50, label='Stringers')

plt.scatter(cx, cy, color='green', marker='x', s=200, linewidth=3, label='Centroid')
plt.title(f'Wing Box Centroid\n({cx:.4f}, {cy:.4f})')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()