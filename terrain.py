from matplotlib import pyplot as plt
import numpy as np

from perlin import octaves as perlin_octaves
from worley import octaves as worley_octaves

from shadow import shadow_onthorgonal, shadow_perspective
from normal_texture import get_normal
from color_improved import get_terrain_color, TerrainColor, TerrainColorGradient

np.set_printoptions(precision=2)

# subtract from all heights their distance to the center
def island_mod(width, height):
    maxD_Sq = np.power((width/2)**2 + (height/2)**2, 1/3)
    center_x = width // 2
    center_y = height// 2

    xs = np.arange(width)
    ys = np.arange(height)
    distance = np.square((center_x - xs)) + np.square((center_y - ys))[:, np.newaxis]
    # return map(distance, 0, maxD_Sq, 1, 0)
    return 1 - (np.power(distance, 1/3) / maxD_Sq)

def generate_terrain(dimension, scale):
    # Geographical customization
    sun_pos = np.array([dimension-20, 20, dimension + dimension], dtype=float)
    sun_pos /= dimension
    shadow_brightness = 0.5
    water_level = 0.3
    slope_cutoff = 0.3

    # Color customization
    # 0.2 gradient different
    color_dict = {
        'water':      TerrainColorGradient(0.0, water_level, np.array([ 98, 166, 169]), np.array([100, 200, 200]), -0.5),
        'sand':       TerrainColorGradient(water_level, 0.4, np.array([241, 182, 158]), np.array([241, 182, 158])*1.2, 0),
        'grass':      TerrainColorGradient(0.4, 0.5, np.array([152, 173,  90])*0.8, np.array([152, 173,  90])*1.2, 0),
        'dark_grass': TerrainColorGradient(0.5, 0.6, np.array([101, 133,  65])*0.8, np.array([101, 133,  65])*1.2, 0),
        'forest':     TerrainColorGradient(0.6, 0.7, np.array([ 71, 118,  69])*0.8, np.array([ 71, 118,  69])*1.2, 0),
        'stone':      TerrainColorGradient(0.7, 0.8, np.array([109, 118, 135])*0.8, np.array([109, 118, 135])*1.2, 0),
        'slate':      TerrainColorGradient(0.8, 0.9, np.array([132, 141, 154])*0.8, np.array([132, 141, 154])*1.2, 0),
        'snow':       TerrainColorGradient(0.9, 1.0, np.array([210, 224, 222]), np.array([210, 224, 222]), 0)
    }

    # Compute Perlin map
    xs = np.linspace(0, scale, dimension, endpoint=False)
    ys = np.linspace(0, scale, dimension, endpoint=False)
    X, Y = np.meshgrid(xs, ys)
    perlin_map = (np.vectorize(perlin_octaves)(X, Y) + 1) / 2
    # worley_map = worley_octaves(dimension, depth=5)

    # Save map?
    # np.save(r"C:\Users\PC\Desktop\Programming\Python\Games\2D Terrain\data\perlinmap_200.npy", perlin_map)

    # Load map?
    terrain_index = 14
    # perlin_map = np.load(rf"C:\Users\PC\Desktop\Programming\Python\Games\2D Terrain\data\perlinmapx500_0.npy")
    # perlin_map = np.load(rf"C:\Users\PC\Desktop\Programming\Python\Games\2D Terrain\data\perlinmap{terrain_index}.npy")
    dimension = perlin_map.shape[0]

    height_map = perlin_map
    # height_map = perlin_map * (1 - worley_map)
    # height_map = (perlin_map - worley_map) / 2

    # height_map /= height_map.max()

    # Raise center to make island
    island_texture = height_map * island_mod(dimension, dimension)
    island_texture /= island_texture.max()

    # Flatten water region for shadow
    flat_water = island_texture.copy()
    water_mask = flat_water < water_level
    flat_water[water_mask] = 0

    # Surface normals(vector3s)
    normal = get_normal(island_texture, dimension, dimension)

    # Colorization based on height
    terrain_color = get_terrain_color(island_texture, color_dict, normal, dimension, dimension, steep_color=color_dict['slate'], slope_cutoff=slope_cutoff, water_level=water_level)
   
    # Shadow
    terrain = shadow_perspective(terrain_color, flat_water, normal, water_mask, dimension, dimension, shadow_brightness, sun_pos, using_normal=True)

    # plt.imshow(terrain_color)
    # plt.imsave(fr"C:\Users\PC\Desktop\Programming\Python\Games\2D Terrain\images\500_b_s.png", terrain)
    plt.imsave(fr"C:\Users\PC\Desktop\Programming\Python\Games\2D Terrain\images\terrain{terrain_index}.png", terrain)
    # plt.show()

generate_terrain(1000, 5)