import numpy as np
from numpy.linalg import norm

# xs, ys, sun_pos must all be normalized
def shadow_onthorgonal(color, height_map, normal_map, water_mask, width, height, shadow_brightness, sun_pos, steps=800, using_normal=False):
    terrain = np.empty((height, width, 3), dtype=float)

    min_step_size = min(1/width, 1/height)

    sun_dir = sun_pos - np.array([0.5, 0.5, 0])
    step_dir = sun_dir / norm(sun_dir)

    for j in range(height):
        print("Line", j)
        for i in range(width):
            height_origin = height_map[j, i]
            p = np.array([i/width, j/height, height_origin])

            in_shadow = False
            for _ in range(steps):
                y_index = int(p[1]*height)
                x_index = int(p[0]*width)
                if x_index < 0 or x_index >= width or y_index < 0 or y_index >= height:
                    break

                h = height_map[y_index, x_index]
                p += step_dir * max(min_step_size, (p[2] - h) * 0.05)

                if h > p[2]:
                    in_shadow = True
                    break
                if p[2] > 1.0:
                    break
            if in_shadow:
                terrain[j, i] = color[j, i] * shadow_brightness
            else:
                if using_normal:
                    if not water_mask[j, i]:
                        normal = normal_map[j, i]
                        normal_shadow = (normal @ (-step_dir) + 1.0) / 2
                        terrain[j, i] = lerp(color[j, i], color[j, i] * shadow_brightness, normal_shadow)
                    else:
                        terrain[j, i] = color[j, i]    
                else:
                    terrain[j, i] = color[j, i]    
    return terrain

def lerp(a, b, t):
    return a + (b - a) * t

def shadow_perspective(color, height_map, normal_map, water_mask, width, height, shadow_brightness, sun_pos, steps=800, using_normal=False):
    terrain = np.empty((height, width, 3), dtype=float)

    min_step_size = min(1/width, 1/height)

    for j in range(height):
        print("Line", j)
        for i in range(width):
            height_origin = height_map[j, i]
            p = np.array([i/width, j/height, height_origin])

            sun_dir = sun_pos - p
            step_dir = sun_dir / norm(sun_dir)

            in_shadow = False
            for _ in range(steps):
                y_index = int(p[1]*height)
                x_index = int(p[0]*width)
                if x_index < 0 or x_index >= width or y_index < 0 or y_index >= height:
                    break

                h = height_map[y_index, x_index]
                p += step_dir * max(min_step_size, (p[2] - h) * 0.05)

                if h > p[2]:
                    in_shadow = True
                    break
                if p[2] > 1.0:
                    break
            if in_shadow:
                terrain[j, i] = color[j, i] * shadow_brightness
            else:
                if using_normal:
                    if not water_mask[j, i]:
                        normal = normal_map[j, i]
                        normal_shadow = (normal @ (-step_dir) + 1.0) / 2
                        terrain[j, i] = lerp(color[j, i], color[j, i] * shadow_brightness, normal_shadow)
                    else:
                        terrain[j, i] = color[j, i]    
                else:
                    terrain[j, i] = color[j, i]    
    return terrain