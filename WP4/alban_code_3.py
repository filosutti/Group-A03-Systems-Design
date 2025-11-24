import numpy as np
import matplotlib.pyplot as plt

def calculate_wingbox_centroid(corners, skin_thickness, skin_density, stringers):
    """
    Calculates the centroid of a hollow wing box cross-section (skins + stringers).
    """
    total_mass = 0
    moment_x = 0
    moment_y = 0

    # Table Header
    print(f"{'Component':<15} {'Len/Area':<12} {'Mass (kg)':<12} {'Centroid (x,y)'}")
    print("-" * 65)

    # --- 1. PROCESS SKINS (Line Segments) ---
    num_points = len(corners)
    for i in range(num_points):
        # Get start and end points
        p1 = corners[i]
        p2 = corners[(i + 1) % num_points]

        # Calculate Length & Midpoint
        L = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        xc_seg = (p1[0] + p2[0]) / 2
        yc_seg = (p1[1] + p2[1]) / 2

        # Calculate Mass (Line Segment)
        m_seg = L * skin_thickness * skin_density

        # Add to totals
        total_mass += m_seg
        moment_x += m_seg * xc_seg
        moment_y += m_seg * yc_seg

        # Print Row
        name = f"Skin {i+1}-{((i+1)%4)+1}"
        print(f"{name:<15} {L:<12.4f} {m_seg:<12.4f} ({xc_seg:.3f}, {yc_seg:.3f})")

    print("-" * 65)

    # --- 2. PROCESS STRINGERS (Point Masses) ---
    for i, s in enumerate(stringers):
        sx, sy, area, s_density = s
        
        # Mass (Point Area)
        m_str = area * s_density
        
        # Add to totals
        total_mass += m_str
        moment_x += m_str * sx
        moment_y += m_str * sy
        
        # Print Row (Formatted to match table)
        name = f"Stringer {i+1}"
        print(f"{name:<15} {area:<12.6f} {m_str:<12.4f} ({sx:.3f}, {sy:.3f})")

    # --- 3. FINAL CALCULATION ---
    if total_mass == 0:
        return (0, 0)

    Cx = moment_x / total_mass
    Cy = moment_y / total_mass

    return (Cx, Cy)

# ==========================================
# INPUTS
# ==========================================

# 1. Geometry: (Front-Bot -> Rear-Bot -> Rear-Top -> Front-Top)
coords = [
    (0.2, -0.02723),  
    (0.7, -0.0066),   
    (0.7, 0.0666),    
    (0.2, 0.08737)    
]

# 2. Material Properties: Al 2024-T81
# from https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA2024T81
# Density: 2.78 g/cc -> 2780 kg/m^3
t_skin = 0.001           # Skin thickness (m)
rho_Al2024 = 2780        # Density (kg/m^3)

# (Stored for future stress/stiffness calcs)
E_Al2024 = 72.4e9        # Young's Modulus (Pa) -> 72.4 GPa
Sigma_Yield = 450e6      # Yield Strength (Pa)  -> ~450 MPa
Sigma_Ult = 485e6        # Ultimate Strength (Pa) -> ~485 MPa

# 3. Stringers (x, y, area, density)
# Using same Al 2024 density for stringers
stringers_data = [
    (0.45, 0.07, 0.0005, rho_Al2024),   # Top stringer
    (0.45, -0.015, 0.0005, rho_Al2024)  # Bottom stringer
]

# ==========================================
# EXECUTION
# ==========================================

centroid = calculate_wingbox_centroid(coords, t_skin, rho_Al2024, stringers_data)

print("="*30)
print(f"FINAL CENTROID: ({centroid[0]:.5f}, {centroid[1]:.5f})")
print("="*30)
print(f"Material: Aluminum 2024-T81 (Rho={rho_Al2024} kg/m^3)")

# ==========================================
# VISUALIZATION CHECK
# ==========================================
x_box = [p[0] for p in coords] + [coords[0][0]]
y_box = [p[1] for p in coords] + [coords[0][1]]

plt.figure(figsize=(10, 6))
plt.plot(x_box, y_box, 'b-', label='Skin (Al 2024-T81)', linewidth=2)
plt.fill(x_box, y_box, alpha=0.1) 

# Plot Stringers
sx = [s[0] for s in stringers_data]
sy = [s[1] for s in stringers_data]
plt.scatter(sx, sy, color='red', s=50, label='Stringers')

# Plot Centroid
plt.scatter(centroid[0], centroid[1], color='green', marker='x', s=200, linewidth=3, label='Calculated Centroid')

plt.title(f'Wing Box Geometry (Al 2024-T81)\nCentroid: ({centroid[0]:.4f}, {centroid[1]:.4f})')
plt.xlabel('Chordwise Position (x)')
plt.ylabel('Vertical Position (y)')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()