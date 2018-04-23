#import pdb
import cv2
import numpy as np
import sys
from paint import paint


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
