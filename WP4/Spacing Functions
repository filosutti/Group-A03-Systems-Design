import numpy as np



#include root and tip as ribs
def rib_places(initial_spacing, total_length, number_of_ribs):
    n = number_of_ribs - 1                   # number of spacings
    
    delta = 2 * (total_length - n * initial_spacing) / (n * (n - 1))
    
    spacings = initial_spacing + delta * np.arange(n)
    
    positions = np.zeros(number_of_ribs)
    positions[1:] = np.cumsum(spacings)
    
    return positions, spacings

#include root and tip as ribs
def spacing_at_position(initial_spacing, total_length, number_of_ribs, position):
    positions, spacings = rib_places(initial_spacing, total_length, number_of_ribs)
    for i in range(len(spacings)):
        if positions[i] <= position < positions[i + 1]:
            return spacings[i]
    # If position is exactly at the tip
    return spacings[-1]