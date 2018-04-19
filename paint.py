import cv2
import numpy as np
import pdb
from random import shuffle


#constants # f_g
GRID_SIZE = 1

# T appoximation_threshold = 100 brush sizes expressed in radii
APPROXIMATION_THRESHOLD = 100

# maximum curved stroke length
MIN_STROKE_LENGTH = 1
MAX_STROKE_LENGTH = 16

# filter constant to limit or exaggerate brush stroke
FILTER_CONSTANT = 1

# methods
DOTTED = 0
CURVED_STROKE = 1

# "Rather than requiring the user to provide a list of brush sizes,
# we found it more useful to use three parameters to specify brush sizes: smallest brush radius R1, number of brushes, and size ratio (Ri+1/Ri)
#smallest brush radius

def generateBrushSizes(smallest_radius, num_brushes, size_ratio):
    brush_sizes = [smallest_radius]
    for brush in range(1, num_brushes):
        last_brush = brush_sizes[-1]
        brush_sizes.append(last_brush * size_ratio)
    return brush_sizes

def paint(image, method, brush_sizes=generateBrushSizes(2, 3, 2)):
    # ensure brush sizes are ordered biggest to smallest
    sorted_brush_sizes = sorted(brush_sizes, reverse=True)

    # create constant colored canvas (black)
    canvas = np.zeros(image.shape)
    for brush_size in sorted_brush_sizes:
        reference_image = referenceImage(image)
        canvas = paintLayer(canvas, reference_image, brush_size, method)

    return canvas


# defined in the paper as
# "convolution  with a  Gaussian kernel of standard deviation f_sigma_R_i
# where f_sigma is some constant factor
# todo: find kernel size, f_sigma
# f_sigma = blur factor
def referenceImage(image, kernel_size=5, f_sigma=100):
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigmaX=f_sigma, sigmaY=f_sigma)
    return blurred_image


def differenceImage(image1, image2):
    difference = np.abs(image1 - image2)
    return difference


# Ri = brush_size
# f_g = grid_step_size
# f_sigma = blur factor
# brush_size is the radius of the brush
def paintLayer(canvas_image, reference_image, brush_size, method):
    # new strokes
    strokes = []

    # create a pointwise difference image
    difference_image = differenceImage(canvas_image, reference_image)

    grid_step_size = GRID_SIZE * brush_size
    grid_half_step = grid_step_size // 2
    rows, columns, _ = reference_image.shape

    for row in range(0, rows, grid_step_size):
      for column in range(0, columns, grid_step_size):
        area_error, largest_error_point_offset = sumError(difference_image, column, row, grid_step_size)

        # if area_error is above the approximation threshold, paint a stroke at this point
        if area_error > APPROXIMATION_THRESHOLD:
          x, y = (largest_error_point_offset[0] + column - grid_half_step, largest_error_point_offset[1] + row - grid_half_step)
          #print x, y, grid_step_size, grid_half_step, largest_error_point_offset

          color = reference_image[y][x]

          # if method was set to curved stroke
          if method == CURVED_STROKE:
              new_stroke = makeCurvedStroke(brush_size, x, y, reference_image, canvas_image)

          # otherwise we are using the dotted stroke
          else:
              new_stroke = makeDottedStroke(brush_size, x, y, color)

          strokes.append(new_stroke)

    layer = paintRandomStrokes(canvas_image, strokes)

    return layer


# sum the error in the region near x,y
def sumError(difference_image, x, y, step):
    neighborhood_limit = step / 2
    M = neighborhood(difference_image, x, y, neighborhood_limit)
    error = np.zeros((M.shape[0], M.shape[1]))
    sum_error = 0
    largest_error = 0
    largest_error_point = neighborhood_limit, neighborhood_limit

    for row in range(0, M.shape[0]):
      for column in range(0, M.shape[1]):
        # find the area error between the current point in the subregion in the blurred image and our canvas value
        blue_error = M[row][column][0].astype(np.int32)
        green_error = M[row][column][1].astype(np.int32)
        red_error = M[row][column][2].astype(np.int32)
        squared_total =  blue_error ** 2 + green_error ** 2 + red_error ** 2
        error = np.sqrt(squared_total)

        # ensure error falls between our valid color range
        clipped_error = np.clip(error, 0, 255)

        # is the point in our difference image or in our reflected border
        M_center = (M.shape[0] // 2, M.shape[1] // 2)
        original_x = x + column - M_center[1]
        original_y = y + row - M_center[0]
        is_row_within_bounds = original_y >= 0 and  original_y < difference_image.shape[1]
        is_column_within_bounds = original_x >= 0 and  original_x < difference_image.shape[0]
        within_image_bounds = is_row_within_bounds and is_column_within_bounds

        if clipped_error > largest_error and within_image_bounds:
            # new largest error found
            largest_error_point = column, row
            largest_error = clipped_error

        sum_error += error

    areaError = sum_error / step ** 2
    return areaError, largest_error_point


def neighborhood(image, x, y, neighborhood_limit):

    method = cv2.BORDER_REFLECT
    padded_image = cv2.copyMakeBorder(image, neighborhood_limit, neighborhood_limit, neighborhood_limit,neighborhood_limit, method)

    padded_image = np.copy(image)
    x_slice = slice(x - neighborhood_limit, x + neighborhood_limit)
    y_slice = slice(y - neighborhood_limit, y + neighborhood_limit)

    return padded_image[y_slice, x_slice]


def paintRandomStrokes(canvas, strokes):
    # randomize strokes
    paint_strokes = np.copy(strokes)
    shuffle(paint_strokes)
    painted_canvas = np.copy(canvas)
    for stroke in paint_strokes:
      # takes a canvas and a paintbrush, and returns the canvas passed with the new stroke painted
      painted_canvas = paintStroke(painted_canvas, stroke)

    return painted_canvas

# this doesn't edit the canvas, just encapsulates the information needed to create a stroke on a canvas later
def makeDottedStroke(brush_size, x, y, color):
    stroke = { 'brush_size': brush_size, 'points': [(x,y)], 'color': color }
    return stroke

def makeCurvedStroke(brush_size, x0, y0, reference_image, canvas_image):
    # our K value in the paper
    stroke_points = [(x0, y0)]

    last_dx = 0
    last_dy = 0
    last_normal = (0, 0)

    # our (x,y) point referenced in the paper
    current_x, current_y = (x0, y0)

     # "the color of the reference image at (x0, y0) is the color of the spline"
    stroke_color = reference_image[y0][x0] 

    for i in range(1, MAX_STROKE_LENGTH):

      # stroke color is the color of the brush at our origin point
      reference_color = reference_image[current_y][current_x]
      canvas_color = canvas_image[current_y][current_x]

      color_diff = differenceImage(grayImage(reference_image), grayImage(canvas_image))[current_y][current_x]
      stroke_luminance = stroke_color[0] * 0.11 + stroke_color[1] * 0.59 + stroke_color[2] * 0.3
      stroke_diff = np.abs(grayImage(reference_image)[current_y][current_x] - stroke_luminance)

      if i > MIN_STROKE_LENGTH and color_diff < stroke_diff:
         break 

      # is this a vanishing gradient?
      # calculate Sobel-filtered luminance of the ref image
      kernel_size = 3
      ddepth = cv2.CV_16S
      gray_reference_image = grayImage(reference_image)
      gradient_x = cv2.Sobel(src=gray_reference_image, ddepth=ddepth, dx=1, dy=0, ksize=kernel_size)
      gradient_y = cv2.Sobel(src=gray_reference_image, ddepth=ddepth, dx=0, dy=1, ksize=kernel_size)
      reference_gradient = gradient_x + gradient_y

      if reference_gradient[current_y][current_x] == 0:
        break

      # calculate the unit vector of the gradient at the current point
      gradient_unit_vector = gradient_x[current_y][current_x], gradient_y[current_y][current_x]

      # calculate the gradient normal at the current point
      gradient_normal = calculateNormal(gradient_unit_vector)

      # reverse the direction of the gradient normal if it is necessary
      if last_normal[0] * gradient_normal[0] + last_normal [1] * gradient_normal[1] < 0:
          gradient_normal = reverseNormal(gradient_normal)

      # impulse response filter (determines curviness of the stroke)
      gradient_normal = impulseResponseFilter(gradient_normal, last_normal, FILTER_CONSTANT)
      new_point = current_x + brush_size * gradient_normal[1], current_y + brush_size * gradient_normal[0]
      stroke_points.append(new_point)

      # remember this normal for the impulse response filter calculation next iteration
      last_normal = gradient_normal

    stroke = { 'brush_size': brush_size, 'points': stroke_points, 'color': stroke_color }

    return stroke


def paintStroke(canvas, stroke):
    # passing thickness of -1 makes a filled circle
    FILLED_CIRCLE = -1
    # color = cv2.cv.Scalar(int(stroke['color'][0]), int(stroke['color'][1]), int(stroke['color'][2]))

    #bug
    # for some reason, stroke looks like [(8, 99)] instead of {} and causes the program to crash

    color = (int(stroke['color'][0]), int(stroke['color'][1]), int(stroke['color'][2]))

    painted_canvas = np.copy(canvas).astype(np.uint8)

    for sp in stroke['points']:
      centroid = (int(sp[0]), int(sp[1]))
      #print centroid
      #print stroke['brush_size']
      #print color
      # print 
      cv2.circle(painted_canvas, centroid, stroke['brush_size'], color, FILLED_CIRCLE)

    return painted_canvas


# calculates the luminance of a color image using the formula provided by hertzmann
def grayImage(image):
    # "The luminance of a pixel is computed with L(r,g,b) = 0.30*r + 0.59*g + 0.11*b"
    gray_image = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    b, g, r = cv2.split(image)
    gray_image =  0.3 * r + 0.59 * g + 0.11 * b
    return gray_image


# calculate a normal
def calculateNormal(gradient):
    return -1 * gradient[1], gradient[0]


# flip a normal 180 degrees
def reverseNormalDirection(normal):
    return -1 * normal


# impulse response filter (determines curviness of the stroke) and limits speckled appearance of short strokes
# filters the stroke direction
def impulseResponseFilter(normal, last_normal, fc):
    normal = fc * normal + (1 - fc) * last_normal
    normal_y, normal_x = normal
    filtered_normal = normal / np.sqrt(normal_x ** 2 + normal_y ** 2)
    return filtered_normal


