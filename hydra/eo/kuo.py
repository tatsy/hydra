'''
Implementation of the paper,
Kuo et al. 2012, "Content-Adaptive Inverse Tone Mapping"
'''

import math
import numpy as np
import scipy as sp
import scipy.ndimage

import hydra.core
import hydra.filter

import matplotlib.pyplot as plt

def kuo_expand_map(L, gamma_removal=-1.0):
    kernel_size = math.ceil(0.1 * max(L.shape))
    Lflt = sp.ndimage.uniform_filter(L, kernel_size)
    epsilon = np.max(Lflt)

    mask = np.ones(L.shape)
    mask[L < epsilon] = 0.0

    mask = sp.ndimage.binary_erosion(mask)

    tmp_expand_map = L * mask

    sigma_s = kernel_size / 5.0
    sigma_r = 100.0 / 255.0
    if gamma_removal > 0.0:
        sigma_r = sigma_r ** gamma_removal

    expand_map = hydra.filter.bilateral(tmp_expand_map, sigma_s, sigma_r, J=L)

    return np.reshape(expand_map, L.shape)

def kuo(img, Lmax, gamma_removal=-1.0):
    if gamma_removal > 0.0:
        img = np.power(img, gamma_removal)

    Ld = hydra.core.lum(img)

    p = 30.0
    Lexp = (Ld * Lmax) / (p * (1.0 - Ld) + Ld)

    expand_map = kuo_expand_map(Ld, gamma_removal)

    Lexp_fit = sp.ndimage.uniform_filter(Lexp, 5)

    Lexp = Lexp_fit * expand_map + Lexp * (1.0 - expand_map)

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:,:,c] = hydra.core.remove_specials(img[:,:,c] * Lexp / Ld)

    return ret
