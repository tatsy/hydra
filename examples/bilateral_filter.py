import scipy as sp
import scipy.misc
import matplotlib.pyplot as plt

import hydra.filter

def main():
    img = sp.misc.imread('../data/lamp.jpg')
    img = img / 255.0

    h, w, _ = img.shape
    sigma_s = max(h, w) * 0.02
    sigma_r = 0.4
    res = hydra.filter.bilateral(img, sigma_s, sigma_r)

    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.axis('off')
    plt.title('Original')

    plt.subplot(1, 2, 2)
    plt.imshow(res)
    plt.axis('off')
    plt.title('Result')

    plt.show()

if __name__ == '__main__':
    main()
