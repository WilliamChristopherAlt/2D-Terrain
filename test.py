import numpy as np
# start = time.time()
# print(f"Terrain {terrain_index} finnished: ", time.time() - start)

vec = np.array([0.4, 2, -4])

print(np.clip(vec, 0, 1))
