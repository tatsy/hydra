import math
from itertools import product
import numpy as np
import scipy as sp
import scipy.misc
import scipy.ndimage
import scipy.sparse
import scipy.sparse.linalg

import hydra.core

EPS = 1.0e-6

def max_quart(mat, percentile):
    n, m = mat.shape
    M = np.sort(mat.reshape(n * m))
    return M[min(round(n * m * percentile), n * m - 1)]

def imresize(img, size):
    if isinstance(size, float):
        size = (int(img.shape[0] * size), int(img.shape[1] * size))

    ret = np.zeros(size)
    for y, x in product(range(size[0]), range(size[1])):
        xx = x / (size[1] - 1) * (img.shape[1] - 1)
        yy = y / (size[0] - 1) * (img.shape[0] - 1)
        ix = int(xx)
        iy = int(yy)
        fx = xx - ix
        fy = yy - iy
        if ix < img.shape[1] - 1 and iy < img.shape[0] - 1:
            ret[y,x] += (1.0 - fx) * (1.0 - fy) * img[iy, ix]
            ret[y,x] += fx * (1.0 - fy) * img[iy, ix+1]
            ret[y,x] += (1.0 - fx) * fy * img[iy+1, ix]
            ret[y,x] += fx * fy * img[iy+1, ix+1]
        else:
            ret[y,x] = img[iy, ix]

    return ret

def divergence(I, method='center'):
    h, w, _ = I.shape
    div = np.zeros((h, w))

    if method == 'center':
        d1 = 1
        d2 = -1
    elif method == 'forward':
        d1 = 1
        d2 = 0
    elif method == 'backward':
        d1 = 0
        d2 = -1
    else:
        raise Exception('Unknown method for divergence!!')

    for y, x in product(range(1,h-1), range(1,w-1)):
        dIdx = (I[y, x+d1, 0] - I[y, x+d2, 0]) / (d1 - d2)
        dIdy = (I[y+d1, x, 1] - I[y+d2, x, 1]) / (d1 - d2)
        div[y,x] = dIdx + dIdy
    return div

def gradient(I, method='center'):
    h, w = I.shape
    grad = np.zeros((h, w, 2))

    if method == 'center':
        d1 = 1
        d2 = -1
    elif method == 'forward':
        d1 = 1
        d2 = 0
    elif method == 'backward':
        d1 = 0
        d2 = -1
    else:
        raise Exception('Unknown method for divergence!!')

    for y, x in product(range(1,h-1), range(1,w-1)):
        dIdx = (I[y, x+d1] - I[y, x+d2]) / (d1 - d2)
        dIdy = (I[y+d1, x] - I[y+d2, x]) / (d1 - d2)
        grad[y,x,0] = dIdx
        grad[y,x,1] = dIdy
    return grad

def calcedge(img):
    G = gradient(img, 'center')
    edge = np.hypot(G[:,:,0], G[:,:,1])
    return edge

def attenuatemap(img, alph, beta, l, levels):
    edge = calcedge(img) / (2.0 ** l)
    tmp = edge / alph
    phi = np.power(edge / alph, beta - 1.0)
    indx = np.isinf(phi)
    phi = hydra.core.remove_specials(phi)
    phi[indx] = np.average(phi)
    if l == levels:
        return phi

    res = imresize(img, 0.5)
    sub = attenuatemap(res, alph, beta, l+1, levels)
    sub = imresize(sub, img.shape)
    return np.multiply(sub, phi)

def gaussseidel(I, divG, maxiter=10):
    h, w = I.shape
    ret = I.copy()

    dx = [ -1, 1, 0, 0 ]
    dy = [ 0, 0, -1, 1 ]
    for it in range(maxiter):
        print('{0:d} / {1:d}'.format(it + 1, maxiter))
        for y, x in product(range(1,h-1), range(1,w-1)):
            cnt = 0
            S = 0.0
            for k in range(4):
                nx = x + dx[k]
                ny = y + dy[k]
                if nx >= 0 and ny >= 0 and nx < w and ny < h:
                    S += ret[ny, nx]
                    cnt += 1
            ret[y,x] = (S - divG[y,x]) / cnt

    return ret

def poisson_solver(f):
    r, c = f.shape
    n = r * c
    b = -f.T.reshape(n)

    A = sp.sparse.spdiags(4.0 * np.ones(n), 0, n, n)
    T = np.ones(n)
    O = T.copy()
    T[range(0,n,r)] = 0.0

    B = sp.sparse.spdiags(-T, 1, n, n) + sp.sparse.spdiags(-O, r, n, n)

    A = A + B + B.T

    x = sp.sparse.linalg.spsolve(A, b)
    x = x.reshape((c, r)).T

    return x

def fattal02(img, beta=0.90, normalize=True):
    Lori = hydra.core.lum(img)
    L = np.log(Lori + 1.0e-6)

    h, w = L.shape
    levels = int(round(math.log2(min(h, w))) - math.log2(32))

    E = calcedge(L)
    alph = 0.1 * np.average(E)

    Phi = attenuatemap(L, alph, beta, 0, levels)

    G = gradient(L, method='forward')
    G[:,:,0] = np.multiply(G[:,:,0], Phi)
    G[:,:,1] = np.multiply(G[:,:,1], Phi)

    divG = hydra.core.remove_specials(divergence(G, method='backward'))

    Ld = np.exp(poisson_solver(divG))
    if normalize:
        Ld = Ld / max_quart(Ld, 0.99995)
        Ld = np.maximum(Ld, 0.0)
        Ld = np.minimum(Ld, 1.0)

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:,:,c] = img[:,:,c] / Lori * Ld

    ret = hydra.core.remove_specials(ret)
    ret = np.maximum(ret, 0.0)
    ret = np.minimum(ret, 1.0)

    return ret
