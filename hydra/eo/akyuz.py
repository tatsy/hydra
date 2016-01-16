'''
Implementation of the paper,
Akyuz et al. 2007, "Do HDR display support LDR content?: a psychophsical evaluation"
'''

import numpy as np

import hydra.core

def akyuz(img, Akyuz_Max=3000, Akyuz_gamma=1.0, gammaRemoval=-1):
    if gammaRemoval > 0.0:
        img = np.power(img, gammaRemoval)

    L = hydra.core.lum(img)
    L_max = np.max(L)
    L_min = np.min(L)

    Lexp = Akyuz_Max * np.power(((L - L_min) / (L_max - L_min)), Akyuz_gamma)

    ret = np.zeros(img.shape)
    for c in range(3):
        ret[:,:,c] = hydra.core.remove_specials(img[:,:,c] * Lexp / L)

    return ret
