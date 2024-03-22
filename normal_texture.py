import numpy as np
from numpy.linalg import norm

# Takes in a height map and returns a normal vector based on surrounding heights
def get_normal(height_map, height, width):
    h = 200
    normal_texture = np.empty((height, width, 3), dtype=float)
    height_map = np.pad(height_map, ((1, 1), (1, 1)), mode='constant', constant_values=0)
    for j in range(height):
        for i in range(width):
            # all indexes move forward by 1
            l = h * height_map[j+1, i  ]
            r = h * height_map[j+1, i+2]
            u = h * height_map[j  , i+1]
            d = h * height_map[j+2, i+1]

            normal = np.array([l-r, u-d, 1.0])
            normal_vec = normal / norm(normal)
            normal_texture[j, i] = normal_vec

    return normal_texture