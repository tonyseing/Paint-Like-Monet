# Paint Like Monet

### Required libraries
* OpenCV
* Numpy

### Objective
The goal of this project was to write a software to generate non-photorealistic rendered images from photograph inputs. The application takes a photograph file as input and outputs an Impressionist-like image.

### Examples
<img art="Two examples of Impressionist renderings from Hertzman's paper" src="https://github.com/tonyseing/Paint-Like-Monet/blob/master/analysis/hertzman_impressionist.png?raw=true" width="600" />

<img src="https://github.com/tonyseing/Paint-Like-Monet/blob/master/output/amy_window.jpg?raw=true" width="300" />
<img src="https://github.com/tonyseing/Paint-Like-Monet/blob/master/output/MIA.jpg?raw=true" width="300" />


### Pipeline
This pipeline creates paintings from photographs by painting successive layers of curved brush strokes using a variety of brush stroke sizes.

The pipeline starts by creating an empty canvas image which is all black, for us to project our impressionist painting onto using Numpy’s np.zeros method. The input image is then convolved over with a Gaussian kernel, via OpenCv’s GaussianBlur method with a reflected border, the output of which will be our reference image when “painting” onto the canvas. 

<img src="https://github.com/tonyseing/Paint-Like-Monet/blob/master/analysis/image_differences_paint.png?raw=true" width="550" />


<img src="https://github.com/tonyseing/Paint-Like-Monet/blob/master/analysis/painting_by_layer.png?raw=true" width="550" />

Brush sizes for our painting are generated based on our smallest radius passed, number of brushes, and the size ratio between successively larger brushes. Input of three brushes, smallest being 1 pixel, and a size ratio of two generates brush sizes of 1, 2, and 4. The Hertzmann paper recommends sizes of 2, 4, and 8 for creating Impressionist-style paintings, so those are the sizes used in this pipeline.


<img src="https://github.com/tonyseing/Paint-Like-Monet/blob/master/analysis/painting_a_brush_stroke.png?raw=true" width="250" />

The program now paints on a number of layers onto our canvas, equal to the number of brush sizes, of the reference image by creating grid points proportional to size of the paint brushes. We create a delta, or difference image, between the reference image and our canvas. Iterating over the grid points over our difference image, the application chooses one point in a region near each grid point with the greatest error, N, and if N’s error is greater than a threshold value, T, I have predetermined, add N’s coordinates to a set of initial brush strokes for this paint layer. This threshold value, T, prevents prevents over-painting areas with a small difference between the reference image and the canvas.


The application reflects the border for points near the edges of the image when calculating neighborhood error. Now, the pipeline randomizes the brush strokes stored for the layer. This is done to prevent creating a uniform appearance in our output. The application then iterates through our stored strokes, and use each stroke’s origin point to begin applying the brush strokes to the canvas. The point stored for each stroke serves as a centroid for the circle point applied to the canvas. The program calculates subsequent points on this brush stroke by calculating the gradient normal at each point, and placing the next point along the angle of the normal, at the distance of the brush radius away. There are two possible gradient normals. The one chosen is the normal that smaller or equal to pi/2. 

A maximum stroke length is predetermined, and this is set to 16 by the recommendation of the Hertzmann paper. This prevents the stroke from adding points on infinitely if it finds a loop. This process is repeated until the predetermined maximum stroke length is reached, or if the color of the next point along the stroke is different than the origin point’s color by a threshold amount.

The stroke is then run through an impulse response filter. This function exaggerates or limits the curvature of a stroke, depending on a predetermined filter constant. The suggested filter constant for creating Impressionist paintings is 1, according to the Hertzmann paper, so that is what is used in my implementation. At this point, the stroke is added to a list.
The program then randomizes the order of stored list of strokes generated. This list of strokes is then applied in its new order onto the canvas. This entire process is applied until the number of brush strokes is exhausted.
The process of opening the files and writing them to disk are performed by the user when he/she runs the program from the command line. The two inputs are the file source location, and the target file location. These are the two manual inputs and the running of the controlling main.py script is the manual portion of the code as it requires the user’s input and actions. 

### Resources
Overview of painterly rendering methods: http://www.mrl.nyu.edu/publications/hertzmann-thesis/hertzmann-thesis-300dpi.pdf  
Painterly Rendering talk: https://www.youtube.com/watch?v=ZmV5gxfQX9E  
Painterly rendering using curved brush strokes: https://www.mrl.nyu.edu/publications/painterly98/hertzmann-siggraph98.pdf  
Smoothing images: https://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html  
Gaussian Blur: https://docs.opencv.org/2.4/modules/imgproc/doc/filtering.html#void%20GaussianBlur(InputArray%20src,%20OutputArray%20dst,%20Size%20ksize,%20double%20sigmaX,%20double%20sigmaY,%20int%20borderType)  
Calculating phase: https://stackoverflow.com/questions/38961957/cv2-phase-gives-the-angle-in-radian
