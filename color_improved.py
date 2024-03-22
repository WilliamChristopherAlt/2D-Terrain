import numpy as np

def ease_out(x):
    return max(0.0, min(1.0, 1 - (1 - x)**6))

def lerp(a, b, t):
    return a + (b - a) * t

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
                terrain[j, i] = lerp(color_dict['sand'].get_color_gradient(height_val), color_dict['water'].get_color_gradient(height_val), water_lerp)
            else:
                if is_flat[j, i]:
                    terrain[j, i] = get_color_by_height(height_val, color_dict)
                else:
                    terrain[j, i] = steep_color.color
    return terrain

# Find a correct for this height, then returns its color
def get_color_by_height(height, color_dict):
    for name, terrain_type in color_dict.items():
        if terrain_type.min_bound <= height and height <= terrain_type.max_bound:
            return terrain_type.get_color_gradient(height)
    return np.array([1,0,1])

class TerrainColor:
    terrains_colors = {}
    def __init__(self, min_bound, max_bound, color:np.ndarray):
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.color = color / 255.9999
        TerrainColor.terrains_colors[(min_bound, max_bound)] = color / 255.9999

    def get_color(self):
        return self.color
    
class TerrainColorGradient:
    terrains_colors = {}
    def __init__(self, min_bound, max_bound, min_color, max_color, lerp_adjust):
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.min_color = np.clip(min_color / 255.999, 0., 1.)
        self.max_color = np.clip(max_color / 255.999, 0., 1.)
        self.lerp_adjust = lerp_adjust
        self.color = (min_color + max_color) / (2 * 255.999)
        # print(self.color, self.min_color, self.max_color)
        # input()

        TerrainColorGradient.terrains_colors[(min_bound, max_bound)] = self
    
    def get_color_gradient(self, height):
        lerp_val = (height - self.min_bound) / (self.max_bound - self.min_bound)
        # print(lerp_val, self.)
        return lerp(self.min_color, self.max_color, lerp_val + self.lerp_adjust)




    # Color customization
    # color_dict = {
    #     'water': Terrain(0.0, water_level, np.array([98, 166, 169])),
    #     'sand': Terrain(water_level, 0.4, np.array([241, 182, 158])),
    #     'grass': Terrain(0.4, 0.5, np.array([152, 173, 90])),
    #     'dark_grass': Terrain(0.5, 0.6, np.array([101, 133, 65])),
    #     'forest': Terrain(0.6, 0.7, np.array([71, 118, 69])),
    #     'stone': Terrain(0.7, 0.8, np.array([109, 118, 135])),
    #     'slate': Terrain(0.8, 0.9, np.array([132, 141, 154])),
    #     'snow': Terrain(0.9, 1.0, np.array([210, 224, 222]))
    # }