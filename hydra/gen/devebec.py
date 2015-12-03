# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import scipy.misc

from .gsolve import *

def remove_specials(img):
    img[np.where(np.isnan(img))] = 0.0
    img[np.where(np.isinf(img))] = 0.0
    return img

def weight_function(img, weight_type):

    if weight_type == 'all':
        weight = np.ones(img.shape)
    elif weight_type == 'hat':
        weight = 1.0 - np.power(2.0 * img - 1.0, 12.0)
    elif weight_type == 'Deb97':
        z_min = 0.0
        z_max = 1.0
        tr = (z_min + z_max) / 2.0
        indx1 = np.where(img <= tr)
        indx2 = np.where(img > tr)
        weight = np.zeros(img.shape)
        weight[indx1] = img[indx1] - z_min
        weight[indx2] = z_max - img[indx2]
        weight[np.where(weight < 0.0)] = 0.0
        weight = weight / weight.max()
    else:
        weight = 1.0

    return weight

def tabled_function(img, table):
    for i in range(3):
        work = np.zeros(img[:,:,i].shape)
        for j in range(256):
            indx = np.where(img[:,:,i] == j)
            work[indx] = table[j, i]
        img[:,:,i] = work
    return img

def combine_ldr(stack, exposure_stack, lin_type, lin_fun, weight_type):
    r, c, col, n = stack.shape
    img_out = np.zeros((r, c, col))
    total_weight = np.zeros((r, c, col))

    for i in range(n):
        tmp_stack = []
        if lin_type == 'gamma2.2':
            tmp_stack = np.power(stack[:,:,:,i] / 255.0, 2.2)
        elif lin_type == 'tabledDeb97':
            tmp_stack = tabled_function(stack[:,:,:,i], lin_fun)
        else:
            raise Exception('Unknown linear type: %s' % lin_type)

        tmp_weight = weight_function(tmp_stack, weight_type)
        img_out = img_out + (tmp_weight * tmp_stack) / exposure_stack[i]
        total_weight = total_weight + tmp_weight

    return remove_specials(img_out / total_weight)

def stack_low_res(stack):
    r, c, col, n = stack.shape
    stack_out = []

    for i in range(n):
        tmp_stack = stack[:,:,:,i]
        tmp_stack = np.round(sp.misc.imresize(tmp_stack, 0.01, 'bilinear'))

        r, c, col = tmp_stack.shape

        if i == 0:
            stack_out = np.zeros((r * c, n, col))

        for j in range(col):
            stack_out[:,i,j] = np.reshape(tmp_stack[:,:,j], (r * c))

    return stack_out

def devebec(images, expotimes, weight_type='all', lin_type='gamma2.2'):
    n_img = len(expotimes)
    if n_img == 0:
        raise Exception('Input images and exposure times are invalid')

    h, w, col = images[0].shape
    stack = np.zeros((h, w, col, n_img))
    for i in range(n_img):
        stack[:,:,:,i] = images[i]

    lin_fun = []
    print('lin_type: %s' % lin_type)
    if lin_type == 'tabledDeb97':
        weight = weight_function(np.array([x / 255.0 for x in range(256)]), weight_type)
        stack2 = stack_low_res(stack)
        lin_fun = np.zeros((256, 3))
        for i in range(3):
            g = gsolve(stack2[:,:,i], expotimes, 10.0, weight)
            lin_fun[:,i] = g / g.max()

    return combine_ldr(stack, np.exp(expotimes) + 1.0, lin_type, lin_fun, weight_type)
