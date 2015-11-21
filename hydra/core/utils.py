"""
Utility functions and commonly-used constants in 'hydra'
"""

EPS = 1.0e-32
INF = 1.0e20

def clamp(x, range=(0.0, 1.0)):
    if range[0] > range[1]:
        raise Exception('Lower bound is larger than upper bound!!')
    return max(range[0], min(x, range[1]))
