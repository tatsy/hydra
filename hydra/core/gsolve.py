# -*- coding: utf-8 -*-
from itertools import product

import numpy as np
import scipy as sp
import scipy.sparse.linalg


def tls(A, b):
    ATA = np.dot(A.T, A)
    ATb = np.dot(A.T, b)
    return sp.sparse.linalg.bicgstab(ATA, ATb)[0]


def gsolve(Z, B, l, w):
    n = 256
    A = np.zeros((Z.shape[0] * Z.shape[1] + n + 1, n + Z.shape[0]), dtype="float")
    b = np.zeros((A.shape[0], 1), dtype="float")

    k = 0
    for i, j in product(range(Z.shape[0]), range(Z.shape[1])):
        wij = w[Z[i, j]]
        A[k, Z[i, j]] = wij
        A[k, n + i] = -wij
        b[k, 0] = wij * B[j]
        k += 1

    A[k, 128] = 1.0
    k += 1

    for i in range(n - 2):
        A[k, i] = l * w[i + 1]
        A[k, i + 1] = -2.0 * l * w[i + 1]
        A[k, i + 2] = l * w[i + 1]
        k += 1

    x = tls(A, b)
    g = np.exp(x[:n])
    return g
