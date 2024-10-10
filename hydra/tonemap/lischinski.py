import numpy as np
import scipy as sp
import numpy.typing as npt
import scipy.sparse
import scipy.sparse.linalg

import hydra.core
from hydra.tonemap import calc_white_point


def minimization(L, g, W, LM_alpha=1.0, LM_lambda=0.4):
    e = 1.0e-4
    r, c = L.shape
    n = r * c

    g = g * W
    b = g.reshape(r * c)

    dy = np.diff(L, n=1, axis=0)
    dy = -LM_lambda / (np.abs(dy) ** LM_alpha + e)
    dy = np.pad(dy, ((0, 1), (0, 0)), "constant")
    dy = dy.reshape(r * c)

    dx = np.diff(L, n=1, axis=1)
    dx = -LM_lambda / (np.abs(dx) ** LM_alpha + e)
    dx = np.pad(dx, ((0, 0), (0, 1)), "constant")
    dx = dx.reshape(r * c)

    A = sp.sparse.spdiags(dx, -r, n, n) + sp.sparse.spdiags(dy, -1, n, n)
    A = A + A.T

    g00 = np.pad(dx, (r, 0), "constant")
    g00 = g00[0:-r]
    g01 = np.pad(dy, (1, 0), "constant")
    g01 = g01[0:-1]

    D = W.reshape(r * c) - (g00 + dx + g01 + dy)
    A = A + sp.sparse.spdiags(D, 0, n, n)

    res = sp.sparse.linalg.spsolve(A, b)
    return res.reshape((r, c))


def lischinski(img: npt.NDArray, alph: float = 0.18) -> npt.NDArray:
    L = hydra.core.lum(img)
    Lwhite = calc_white_point(L)
    Lwhite2 = Lwhite * Lwhite

    maxL = np.max(L)
    minL = np.min(L)
    eps = 1.0e-6
    minLLog = np.log2(minL + eps)
    Z = np.ceil(np.log2(maxL) - minLLog)

    fstopMap = np.zeros(L.shape)
    Lav = hydra.core.log_mean(L)

    for i in range(Z):
        indx = np.logical_and(L >= 2 ** (i - 1 + minLLog), L < 2 ** (minLLog + i))
        if indx.any():
            Rz = hydra.core.max_quart(L[indx], 0.5)
            Rz2 = alph * Rz / Lav
            f = (Rz2 * (1.0 + Rz2 / Lwhite2)) / (1.0 + Rz2)

            fstopMap[indx] = np.log(f / Rz)

    fstopMap = 2.0 ** minimization(np.log2(L + eps), fstopMap, 0.07 * np.ones(L.shape))

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:, :, c] = img[:, :, c] * fstopMap

    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)

    return ret
