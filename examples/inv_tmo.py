import numpy as np
import scipy as sp
import scipy.misc

import hydra.io
import hydra.eo

def main():
    img = sp.misc.imread('../data/lamp.jpg') / 255.0
    hdr = hydra.eo.akyuz(img)
    hydra.io.save('lamp.hdr', hdr)

if __name__ == '__main__':
    main()
