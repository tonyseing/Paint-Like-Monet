import pdb
import cv2
import numpy as np
import sys
from paint import paint
from matplotlib import pyplot as plt


# methods
# need to abstract this out into a constants file
DOTTED_STROKE = 0
CURVED_STROKE = 1

def main():
    try:
        if len(sys.argv) <= 1:
            raise FileNotSpecified("No input file specified")

        elif len(sys.argv) <= 2:
            raise FileNotSpecified("No output file specified")

        image_name = sys.argv[1]
        output_name = sys.argv[2]

        # read in the image
        image = cv2.imread(image_name, cv2.IMREAD_COLOR)

        # create the painting
        painted_image = paint(image, CURVED_STROKE)

        # display it for testing
        """
        cv2.imshow('image', painted_image)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', 1200, 800)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """

        # write image to disk
        cv2.imwrite(output_name, painted_image)

    except FileNotSpecified:
        print "Error: Either input or output file not specified"
        sys.exit()

class FileNotSpecified(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


main()
