import numpy as np
import numpy.typing as npt


def gamma(L: npt.NDArray, g: float) -> npt.NDArray:
    return np.power(L, g)
