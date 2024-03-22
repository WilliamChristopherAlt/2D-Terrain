import random
import numpy as np

permutation = list(range(256))
random.shuffle(permutation)

p = np.empty((512), dtype=int)
for i in range(512):
    p[i] = permutation[i%256]

def fade(t):
    # return t*t*(3-2*t)
    return t*t*t * (t * (t*6 - 15) + 10)

def grad(hash, x, y):
    # 3 = 0b11
    hash &= 3
    if   hash == 0: return  x
    elif hash == 1: return -x
    elif hash == 2: return  y
    elif hash == 3: return -y
    return 0

def lerp(a, b, t):
    # return a + t * (b - a)
    return (b - a) * (3.0 - t * 2.0) * t * t + a

def noise(x, y):
    xi = int(x) & 255
    yi = int(y) & 255
    xf = x - int(x)
    yf = y - int(y)
    u = fade(xf)
    v = fade(yf)

    aa = p[p[xi  ] + yi  ]
    ba = p[p[xi+1] + yi  ]
    ab = p[p[xi  ] + yi+1]
    bb = p[p[xi+1] + yi+1]

    y1 = lerp(grad(aa, xf, yf  ), grad(ba, xf-1, yf  ), u)
    y2 = lerp(grad(ab, xf, yf-1), grad(bb, xf-1, yf-1), u)
    return lerp(y1, y2, v)
    
def octaves(x, y, depth=7):
    accum = 0.0
    frequency = 1
    weight = 1.0
    max_val = 0

    for i in range(depth):
        accum += weight * noise(x * frequency, y * frequency)
        weight *= 0.5
        frequency *= 2
        max_val += weight
    
    return accum / max_val