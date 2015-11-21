import math
from .utils import *

class Pixel(object):
    def __init__(self, r, g, b):
        d = max(r, max(g, b))
        if (d < EPS):
            self.r = 0
            self.g = 0
            self.b = 0
            self.e = 0
            return

        m, ie = math.frexp(d)
        d = m * 256.0 / d

        self.r = int(clamp(r * d, (0, 255)))
        self.g = int(clamp(g * d, (0, 255)))
        self.b = int(clamp(b * d, (0, 255)))
        self.e = int(clamp(ie + 128, (0, 255)))

    def get(self, i):
        return self.__getitem__(i)

    def __getitem__(self, i):
        if i == 0: return self.r
        if i == 1: return self.g
        if i == 2: return self.b
        if i == 3: return self.e
        raise Exception('Pixel has only 4 channels. {0} specified.'.format(i))
