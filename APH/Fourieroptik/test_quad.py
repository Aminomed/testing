import numpy as np
from scipy.integrate import quad

d = 1
Y = np.linspace(-1, 1, 400) * d

def spalt(k, y):
    return d / np.pi * np.sin(k * d / 2) / (k * d / 2) * np.cos(y * k)

y = Y[0]
print(quad(spalt, 0, 2 * np.pi * 3 / d, args=(y,)))
