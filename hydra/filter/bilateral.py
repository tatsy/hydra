"""
Implementation of the paper,

Gastal et al. 2011,
"Domain Transform for Edge-Preserving Image and Video Processing"
"""

import math
import numpy as np

def rec_filter_horizontal(I, D, sigma):
    a = math.exp(-math.sqrt(2.0) / sigma)

    F = I.copy()
    V = np.power(a, D)

    h, w, num_channels = I.shape

    for i in range(1,w):
        for c in range(num_channels):
            F[:,i,c] = F[:,i,c] + V[:,i] * (F[:,i-1,c] - F[:,i,c])

    for i in range(w-2,-1,-1):
        for c in range(num_channels):
            F[:,i,c] = F[:,i,c] + V[:,i+1] * (F[:,i+1,c] - F[:,i,c])

    return F

def bilateral(I, sigma_s, sigma_r, num_iterations=5, J=None):
    if I.ndim == 3:
        img = I.copy()
    else:
        h, w = I.shape
        img = I.reshape((h, w, 1))

    if J is None:
        J = img

    if J.ndim == 2:
        h, w = J.shape
        J = np.reshape(J, (h, w, 1))

    h, w, num_channels = J.shape

    dIcdx = np.diff(J, n=1, axis=1)
    dIcdy = np.diff(J, n=1, axis=0)

    dIdx = np.zeros((h, w))
    dIdy = np.zeros((h, w))

    for c in range(num_channels):
        dIdx[:,1:] = dIdx[:,1:] + np.abs(dIcdx[:,:,c])
        dIdy[1:,:] = dIdy[1:,:] + np.abs(dIcdy[:,:,c])

    dHdx = (1.0 + sigma_s / sigma_r * dIdx)
    dVdy = (1.0 + sigma_s / sigma_r * dIdy)

    dVdy = dVdy.T

    N = num_iterations
    F = img.copy()

    sigma_H = sigma_s

    for i in range(num_iterations):
        sigma_H_i = sigma_H * math.sqrt(3.0) * (2.0 ** (N - (i + 1))) / math.sqrt(4.0 ** N - 1.0)

        F = rec_filter_horizontal(F, dHdx, sigma_H_i)
        F = np.swapaxes(F, 0, 1)
        F = rec_filter_horizontal(F, dVdy, sigma_H_i)
        F = np.swapaxes(F, 0, 1)

    return F
