import math

import numpy as np

from hydra.core.utils import EPS


class Pixel(object):
    def __init__(self, r: float, g: float, b: float) -> None:
        self.r: int
        self.g: int
        self.b: int
        self.e: int

        d = max(r, max(g, b))
        if d < EPS:
            self.r = 0
            self.g = 0
            self.b = 0
            self.e = 0
            return

        m, ie = np.frexp(d)
        d = m * 256.0 / d

        self.r = int(np.clip(r * d, 0, 255))
        self.g = int(np.clip(g * d, 0, 255))
        self.b = int(np.clip(b * d, 0, 255))
        self.e = int(np.clip(ie + 128, 0, 255))

    def get(self, i: int) -> int:
        return self.__getitem__(i)

    def __getitem__(self, i: int) -> int:
        if i == 0:
            return self.r
        if i == 1:
            return self.g
        if i == 2:
            return self.b
        if i == 3:
            return self.e

        raise IndexError(f"Pixel has only 4 channels. {i:d} specified.")
