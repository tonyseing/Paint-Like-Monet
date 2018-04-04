import cv2
import numpy as np
import pdb





# brush sizes expressed in radii
default_brush_sizes = [1, 2, 3]

def paint(image, brush_sizes=default_brush_sizes):
    # ensure brush sizes are ordered biggest to smallest
    sorted_brush_sizes = sorted(brush_sizes, reverse=True)

    # create constant colored canvas (black)
    canvas = np.zeros(image.shape)
    reference_image = referenceImage(image)
    cv2.imshow('image', reference_image)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1200, 800)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# defined in the paper as
# "convolution  with a  Gaussian kernel of standard deviation f_sigma_R_i
# where f_sigma is some constant factor
def referenceImage(image, kernel_size=5, f_sigma=100):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigmaX=f_sigma, sigmaY=f_sigma)
    return blurred_image

def paintLayer(canvas_image, reference_image, Ri):
    #
    return 0

def makeSplineStroke(x0, y0, R, reference_image):
    #
    return 0
