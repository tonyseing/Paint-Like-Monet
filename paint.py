import cv2
import numpy as np
import pdb
from random import shuffle

#constants # f_g
grid_size = 1
# T appoximation_threshold = 100 brush sizes expressed in radii
approximation_threshold = 100

# "Rather than requiring the user to provide a list of brush sizes,
# we found it more useful to use three parameters to specify brush sizes: smallest brush radius R1, number of brushes, and size ratio (Ri+1/Ri)
#smallest brush radius



def generateBrushSizes(smallest_radius, num_brushes, size_ratio):
    brush_sizes = [smallest_radius]
    for brush in range(1, num_brushes):
        last_brush = brush_sizes[-1]
        brush_sizes.append(last_brush * size_ratio)
    return brush_sizes

def paint(image, brush_sizes=generateBrushSizes(2, 3, 2)):
    # ensure brush sizes are ordered biggest to smallest
    sorted_brush_sizes = sorted(brush_sizes, reverse=True)

    # create constant colored canvas (black)
    canvas = np.zeros(image.shape)
    for brush_size in sorted_brush_sizes:
        reference_image = referenceImage(image)
        canvas = paintLayer(canvas, reference_image, brush_size)


    cv2.imshow('image', reference_image)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1200, 800)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# defined in the paper as
# "convolution  with a  Gaussian kernel of standard deviation f_sigma_R_i
# where f_sigma is some constant factor
# todo: find kernel size, f_sigma
# f_sigma = blur factor
def referenceImage(image, kernel_size=5, f_sigma=100):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigmaX=f_sigma, sigmaY=f_sigma)
    return blurred_image

def differenceImage(image1, image2):
    pdb.set_trace()
    difference = image1 - image2
    cv2.imshow('image', difference)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 1200, 800)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return difference

# Ri = brush_size
# f_g = grid_step_size
# f_sigma = blur factor
# brush_size is the radius of the brush
def paintLayer(canvas_image, reference_image, brush_size):
    # new strokes
    strokes = []

    # create a pointwise difference image
    difference_image = differenceImage(canvas_image, reference_image)

    grid_step_size = grid_size * brush_size
    rows, columns, _ = reference_image.shape
    for row in range(0, rows, grid_step_size):
      for column in range(0, columns, grid_step_size):
        area_error, largest_error_point = sumError(reference_image, column, row, grid_step_size)
        # if area_error is above the approximation threshold, paint a stroke at this point
        if area_error > approximation_threshold:
          x, y = largest_error_point
          new_stroke = makeStroke(brush_size, x, y, reference_image)
          strokes.append(new_stroke)

    paintRandomStrokes(canvas_image, strokes)

def paintRandomStrokes(canvas, strokes):
    # randomize strokes
    pdb.set_trace()
    paint_strokes = np.copy(strokes)
    shuffle(paint_strokes)

    #todo, actually place the strokes on the canvas and return finished image

# this doesn't edit the canvas, just encapsulates the information needed to create a stroke on a canvas later
def makeStroke(brush_size, x, y, reference_image):
    return reference_image

# sum the error in the region near x,y
def sumError(image, x, y, step):
    M = neighborhood(image, x, y, step)
    error = np.zeros((M.shape[0], M.shape[1]))
    current_value = image[y][x]
    areaError = 0
    largest_error = 0
    largest_error_point = None

    for row in range(M.shape[0]):
      for column in range(M.shape[1]):
        # find the area error between the current point in the subregion and our current value at x,y
        blue, green, red = current_value
        m_blue, m_green, m_red = M[row][column]
        error = np.sqrt((m_blue-blue) ** 2 + (m_green-green) ** 2 + (m_red - red) ** 2)
        # clip the error
        clipped_error = np.clip(error, 0, 255)

        if clipped_error > largest_error:
            # new largest error found
            largest_error_point = row, column
            largest_error = clipped_error

        areaError += error
    return areaError, largest_error_point

def neighborhood(image, x, y, step):
    x_slice = slice(x-step/2, x+step/2)
    y_slice = slice(y-step/2, y+step/2)
    return image[x_slice, y_slice]

def makeSplineStroke(x0, y0, R, reference_image):
    #
    return 0
