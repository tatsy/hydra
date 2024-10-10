import os

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

import hydra.filters

ROOT_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir)
IMAGE_PATH = os.path.join(ROOT_DIR, "data", "lamp.jpg")


def main():
    img = Image.open(IMAGE_PATH)
    img = np.array(img, dtype="uint8")
    img = img / 255.0

    h, w, _ = img.shape
    sigma_s = max(h, w) * 0.02
    sigma_r = 0.4
    res = hydra.filters.bilateral(img, sigma_s, sigma_r)

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.imshow(img)
    ax.axis("off")
    ax.set_title("Original")

    ax = fig.add_subplot(122)
    ax.imshow(res)
    ax.axis("off")
    ax.set_title("Result")

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
