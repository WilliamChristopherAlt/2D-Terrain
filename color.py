import numpy as np

def ease_out(x):
    return max(0.0, min(1.0, 1 - (1 - x)**6))

def lerp(a, b, t):
    # return a + (a - b) * t
    return (1 - t) * a + t * b

def get_terrain_color(texture, color_dict, normal, width, height, steep_color, slope_cutoff, water_level):
    flatness = np.sum(normal * np.array([0, 0, 1]), axis=-1)
    is_flat = flatness > slope_cutoff
    water_mask = texture < water_level

    terrain = np.zeros(shape=(height, width, 3), dtype=float)

    for j in range(height):
        for i in range(width):
            height_val = texture[j, i]
            if water_mask[j, i]:
                water_depth = water_level - height_val
                water_lerp = ease_out(water_depth/water_level)
                terrain[j, i] = lerp(color_dict['sand'], color_dict['water'], water_lerp)
            else:
                if is_flat[j, i]:
                    if height_val < 0.4:
                        terrain[j, i] = color_dict['sand']
                    elif height_val < 0.5:
                        terrain[j, i] = color_dict['grass']
                    elif height_val < 0.6:
                        terrain[j, i] = color_dict['dark_grass']
                    elif height_val < 0.7:
                        terrain[j, i] = color_dict['forest']
                    elif height_val < 0.8:
                        terrain[j, i] = color_dict['stone']
                    elif height_val < 0.9:
                        terrain[j, i] = color_dict['slate']
                    else:
                        terrain[j, i] = color_dict['snow']
                else:
                    terrain[j, i] = color_dict[steep_color]
    return terrain