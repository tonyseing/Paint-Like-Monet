import cv2
import numpy as np
import pdb



# brush sizes expressed in radii
default_brush_sizes = [1, 2, 3]

# "Rather than requiring the user to provide a list of brush sizes,
# we found it more useful to use three parameters to specify brush sizes: smallest brush radius R1, number of brushes, and size ratio (Ri+1/Ri)
#smallest brush radius
# 
def generateBrushSizes(smallest_radius, num_brushes, size_ratio):
    brush_sizes = [smallest_radius]
    for brush in range(1, num_brushes):
        last_brush = brush_sizes[-1]
        brush_sizes.append(last_brush * size_ratio)
    return brush_sizes

def paint(image, brush_sizes=generateBrushSizes(1.0, 3, 1.4)):
    pdb.set_trace()
    # ensure brush sizes are ordered biggest to smallest
    sorted_brush_sizes = sorted(brush_sizes, reverse=True)

    # create constant colored canvas (black)
    canvas = np.zeros(image.shape)
    for brush_size in sorted_brush_sizes:
        reference_image = referenceImage(image)
        paintLayer(canvas, reference_image, brush_size)

    cv2.imshow('image', reference_image)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1200, 800)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# defined in the paper as
# "convolution  with a  Gaussian kernel of standard deviation f_sigma_R_i
# where f_sigma is some constant factor
# todo: find kernel size, f_sigma
def referenceImage(image, kernel_size=5, f_sigma=100):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigmaX=f_sigma, sigmaY=f_sigma)
    return blurred_image

def paintLayer(canvas_image, reference_image, Ri):
    #
    return 0

def makeSplineStroke(x0, y0, R, reference_image):
    #
    return 0
