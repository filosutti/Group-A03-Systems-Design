import numpy as np
import matplotlib.pyplot as plt
coords = [
    (0.2, -0.02723), (0.7, -0.0066),   
    (0.7, 0.0666),   (0.2, 0.08737)    
]
t_skin = 0.001
rho_Al2024 = 2780
n_stringers_side = 10 #change this for wing box geometry 
L_stringer = 1/25           #0.25 of this offset to inside for centroid of point area of stringer
t_stringer = 2*(10**(-3))
A_stringer = ((L_stringer * t_stringer)*2) - (t_stringer**2)  #approx area of L shape stringer

##########################################
# FUNCTION TO CALCULATE CENTROID
##########################################

def calculate_wingbox_centroid(corners, skin_thickness, skin_density, n_str, A_str, L_str):
    total_mass = 0
    moment_x = 0
    moment_y = 0

    # print(f"{'Component':<15} {'Len/Area':<12} {'Mass (kg)':<12} {'Centroid (x,y)'}")
    # print("-" * 65)

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

        # print(f"Skin {i+1}-{((i+1)%4)+1:<9} {L:<12.4f} {m_seg:<12.4f} ({xc_seg:.3f}, {yc_seg:.3f})")

    # print("-" * 65)

    # --- 2. STRINGERS ---
    # Top Skin: corners[3] -> corners[2]
    # Bot Skin: corners[0] -> corners[1]
    segments = [
        (corners[3], corners[2], "Top"), 
        (corners[0], corners[1], "Bot")
    ]
    
    stringer_coords = [] 
    count = 1
    offset_dist = L_str * 0.25  # The 1/4 offset magnitude

    for p_start, p_end, side in segments:
        for i in range(1, n_str + 1):
            f = i / (n_str + 1)
            
            # Base Position on Skin
            sx = p_start[0] + f * (p_end[0] - p_start[0])
            sy = p_start[1] + f * (p_end[1] - p_start[1])

            # Apply Offset Towards Middle
            # If Top, go down (-). If Bot, go up (+).
            if side == "Top":
                sy -= offset_dist
            else:
                sy += offset_dist
            
            # Mass & Moments
            m_str = A_str * skin_density
            total_mass += m_str
            moment_x += m_str * sx
            moment_y += m_str * sy
            
            stringer_coords.append((sx, sy))
            # print(f"Stringer {count:<6} {A_str:<12.6f} {m_str:<12.4f} ({sx:.3f}, {sy:.3f})")
            count += 1

    # --- 3. FINAL CALCULATION ---
    if total_mass == 0: return 0, 0, []

    Cx = moment_x / total_mass
    Cy = moment_y / total_mass

    return Cx, Cy, stringer_coords


# ==========================================
# EXECUTION
# ==========================================

cx, cy, str_coords = calculate_wingbox_centroid(coords, t_skin, rho_Al2024, n_stringers_side, A_stringer, L_stringer)

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

if str_coords:
    sx_list, sy_list = zip(*str_coords)
    plt.scatter(sx_list, sy_list, color='red', s=50, label='Stringers')

plt.scatter(cx, cy, color='green', marker='x', s=200, linewidth=3, label='Centroid')
plt.title(f'Wing Box Centroid\n({cx:.4f}, {cy:.4f})')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()