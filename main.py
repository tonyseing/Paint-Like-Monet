import pdb
import cv2
import numpy as np
import sys
from matplotlib import pyplot as plt




def main():
    try:
        if len(sys.argv) <= 1:
            raise FileNotSpecified("No input file specified")

        image_name = sys.argv[1]

        # read in the image
        image = cv2.imread(image_name, cv2.IMREAD_COLOR)
        # plt.imshow(image, cmap = 'gray', interpolation = 'bicubic')

    except FileNotSpecified:
        print "Error: File not specified"
        sys.exit()

class FileNotSpecified(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


main()
