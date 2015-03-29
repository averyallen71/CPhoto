import numpy as np
import scipy as sp
import scipy.signal
import cv2

def generatingKernel(parameter):
  """ 

  Args:
    parameter (float): Range of value: [0, 1].

  Returns:
    numpy.ndarray: A 5x5 kernel.

  """
  kernel = np.array([0.25 - parameter / 2.0, 0.25, parameter,
                     0.25, 0.25 - parameter /2.0])
  return np.outer(kernel, kernel)

def reduce(image):
  """
  
  Args:
    image (numpy.ndarray): a grayscale image of shape (r, c)

  Returns:
    output (numpy.ndarray): an image of shape (ceil(r/2), ceil(c/2))
      For instance, if the input is 5x7, the output will be 3x4.

  """
  # WRITE YOUR CODE HERE.
  row_count = len(image)
  col_count = len(image[0])
  kernel = generatingKernel(.4)
  blurred = scipy.signal.convolve2d(image, kernel, 'same')
  output = np.zeros((np.ceil(row_count/2.0), np.ceil(col_count/2.0)), dtype = np.float64)
  output_row_count = len(output)
  output_col_count = len(output[0])  

  i = 0
  j = 0
  for row in range(0, row_count,2):
    for column in range(0, col_count,2):
      pixel = blurred[row][column]
      output[i][j] = pixel
      j += 1
      if j == output_col_count:
        j = 0
        i += 1
  return output


  # END OF FUNCTION.

def gaussPyramid(image, levels):
  """ Construct a pyramid from the image by reducing it by the number of levels
  passed in by the input.

  Note: You need to use your reduce function in this function to generate the
  output.

  Args:
    image (numpy.ndarray): A grayscale image of dimension (r,c) and dtype float.
    levels (uint8): A positive integer that specifies the number of reductions
                    you should do. So, if levels = 0, you should return a list
                    containing just the input image. If levels = 1, you should
                    do one reduction. len(output) = levels + 1

  Returns:
    output (list): A list of arrays of dtype np.float. The first element of the
                   list (output[0]) is layer 0 of the pyramid (the image
                   itself). output[1] is layer 1 of the pyramid (image reduced
                   once), etc. We have already included the original image in
                   the output array for you. The arrays are of type
                   numpy.ndarray.

  Consult the lecture and README for more details about Gaussian Pyramids.
  """
  output = [image]
  # WRITE YOUR CODE HERE.
  for i in range(levels):
    output.append(reduce(output[i]))
  return output
  # END OF FUNCTION.
