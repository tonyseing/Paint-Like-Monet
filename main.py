import pdb
import cv2
import numpy as np
import sys
from paint import paint
from matplotlib import pyplot as plt




def main():
    try:
        if len(sys.argv) <= 1:
            raise FileNotSpecified("No input file specified")

        image_name = sys.argv[1]

        # read in the image
        image = cv2.imread(image_name, cv2.IMREAD_COLOR)
        painted_image = paint(image)
        cv2.imshow('image', painted_image)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 1200, 800)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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
