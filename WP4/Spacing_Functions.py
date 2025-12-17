import numpy as np



#include root and tip as ribs
def rib_places(initial_spacing, total_length, number_of_ribs, space_free_at_end):
    # number of spacings between ribs
    n = number_of_ribs - 1 if space_free_at_end == 0 else number_of_ribs - 2

    delta = 2 * (total_length - space_free_at_end - n * initial_spacing) / (n * (n - 1))

    spacings = initial_spacing + delta * np.arange(n)

    # rib positions (excluding final free end)
    positions = np.zeros(n + 1)
    positions[1:] = np.cumsum(spacings)

    # add final point at total_length
    positions = np.append(positions, total_length)

    spacings = np.append(spacings, space_free_at_end)

    return positions, spacings

print(positions, spacings)

#include root and tip as ribs
def spacing_at_position(initial_spacing, total_length, number_of_ribs, position, space_free_at_end):
    positions, spacings = rib_places(initial_spacing, total_length, number_of_ribs, space_free_at_end)
    for i in range(len(spacings)):
        if positions[i] <= position < positions[i + 1]:
            return spacings[i]
    # If position is exactly at the tip
    return spacings[-1]

