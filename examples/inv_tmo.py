import numpy as np
from PIL import Image

import hydra.eo
import hydra.io


def main():
    img = Image.open("../data/lamp.jpg")
    img = np.array(img, dtype="uint8")
    img = img / 255.0
    hdr = hydra.eo.akyuz(img)
    hydra.io.save("lamp.hdr", hdr)


if __name__ == "__main__":
    main()
