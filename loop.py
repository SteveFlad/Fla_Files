import numpy as np

def periodic_function(p):
    """Maps sine function to a usable range for object size."""
    return np.interp(np.sin(2 * np.pi * p), [-1, 1], [2, 8])

def offset(x, y, width, height):
    """Calculate offset based on distance from the center."""
    center_x, center_y = width / 2, height / 2
    return 0.01 * np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

import matplotlib.pyplot as plt

# Parameters
num_frames = 60
grid_size = 40
width, height = 500, 500

# Create figure
fig, ax = plt.subplots()
plt.axis("equal")
plt.axis("off")

# Generate frames
for frame in range(num_frames):
    plt.cla()
    t = frame / num_frames
    
    for i in range(grid_size):
        for j in range(grid_size):
            x = np.interp(i, [0, grid_size - 1], [0, width])
            y = np.interp(j, [0, grid_size - 1], [0, height])
            
            size = periodic_function(t - offset(x, y, width, height))
            ax.plot(x, y, 'o', markersize=size, color="black")

    plt.pause(0.1)

plt.show()
