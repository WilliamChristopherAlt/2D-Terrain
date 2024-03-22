import numpy as np

def noise(texture_dimension, no_cells):
    cells = np.random.randint(0, texture_dimension, (no_cells, 2))

    xs = np.arange(0, texture_dimension)
    ys = np.arange(0, texture_dimension)
    x_square = np.square(cells[:, 0, np.newaxis] - xs)
    y_square = np.square(cells[:, 1, np.newaxis] - ys)

    distance = x_square[:, :, np.newaxis] + y_square [:, np.newaxis, :]
    texture = np.sqrt(np.min(distance, axis=0))
    texture /= texture.max()

    return texture

def octaves(dimension, no_Cells=20, depth=5):
    weight = 1.0
    max_val = 0

    texture = np.zeros((dimension, dimension), dtype=float)

    for i in range(depth):
        texture += weight * noise(dimension, no_Cells)
        max_val += weight
        weight *= 0.5
        no_Cells *= 2
    
    return texture / max_val