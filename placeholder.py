import numpy as np
from numpy.linalg import norm

def get_shadow_mask(height_map, width, height, xs, ys, sun_pos, steps=800):
    shadow_mask = np.zeros_like(height_map, dtype=bool)
    min_step_size = min(1/width, 1/height)

    sun_dir = sun_pos - np.array([0.5, 0.5, 0])
    step_dir = sun_dir / norm(sun_dir)

    for j in range(height):
        print("Line", j)
        for i in range(width):
            height_origin = height_map[j, i]
            p = np.array([xs[i], ys[j], height_origin])
            for _ in range(steps):
                y_index = int(p[1]*height)
                x_index = int(p[0]*width)
                if x_index < 0 or x_index >= width or y_index < 0 or y_index >= height:
                    break

                h = height_map[y_index, x_index]
                p += step_dir * max(min_step_size, (p[2] - h) * 0.05)

                if h > p[2]:
                    shadow_mask[j, i] = True
                    break
                if p[2] > 1.0:
                    break
    return shadow_mask
                