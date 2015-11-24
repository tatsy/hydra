"""
Example 2. Load and save
"""

import hydra.io

filename = '../data/memorial.hdr'

def main():
    # Load HDR
    img = hydra.io.load(filename)

    # Save HDR
    hydra.io.save('image.hdr', img)

if __name__ == '__main__':
    main()
