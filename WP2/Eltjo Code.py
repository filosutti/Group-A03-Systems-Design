import numpy as np

M_cruise = 0.77

sweep_angle_quarter_chord = np.arccos(1.16 / (M_cruise + 0.5))
sweep_angle_quarter_chord_deg = np.degrees(sweep_angle_quarter_chord)
taper_ratio = 0.2*(2-sweep_angle_quarter_chord_deg*(np.pi/180))




