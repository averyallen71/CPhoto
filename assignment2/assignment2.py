# ASSIGNMENT 2
# Robert Avery Allen
# 902649920

import cv2
import numpy as np
import scipy as sp

""" Assignment 2 - Basic Image Input / Output / Simple Functionality

This file has a number of functions that you need to fill out in order to
complete the assignment. Please write the appropriate code, following the
instructions on which functions you may or may not use.
"""

def numberOfPixels(image):
    """ This function returns the number of pixels in a grayscale image.

    Note: A grayscale image has one dimension as covered in the lectures. You
    DO NOT have to account for a color image.

    You may use any / all functions to obtain the number of pixels in the image.

    Args:
        image (numpy.ndarray): A grayscale image represented in a numpy array.

    Returns:
        int: The number of pixels in an image.
    """
    # WRITE YOUR CODE HERE.
    count = 0
    for i in range(len(image)):
        count += len(image[i])
    return count
    # END OF FUNCTION.

def averagePixel(image):
    """ This function returns the average color value of a grayscale image.

    Assignment Instructions: In order to obtain the average pixel, add up all
    the pixels in the image, and divide by the total number of pixels. We advise
    that you use the function you wrote above to obtain the number of pixels!

    You may not use numpy.mean or numpy.average. All other functions are fair
    game.

    Args:
        image (numpy.ndarray): A grayscale image represented in a numpy array.

    Returns:
        int: The average pixel in the image (Range of 0-255).
    """
    # WRITE YOUR CODE HERE.
    rows = len(image)
    columns = len(image[0])
    total = 0
    for i in range(rows):
        for j in range(columns):
            total += image[i][j]
    return int(total/numberOfPixels(image))
    # END OF FUNCTION.

def convertToBlackAndWhite(image):
    """ This function converts a grayscale image to black and white.

    Assignment Instructions: Iterate through every pixel in the image. If the
    pixel is strictly greater than 128, set the pixel to 255. Otherwise, set the
    pixel to 0. You are essentially converting the input into a 1-bit image, as 
    we discussed in lecture, it is a 2-color image.

    You may NOT use any thresholding functions provided by OpenCV to do this.
    All other functions are fair game.

    Args:
        image (numpy.ndarray): A grayscale image represented in a numpy array.

    Returns:
        numpy.ndarray: The black and white image.
    """
    # WRITE YOUR CODE HERE.
    rows = len(image)
    columns = len(image[0])
    for i in range(rows):
        for j in range(columns):
            if image[i][j] > 128:
                image[i][j] = 255
            else:
                image[i][j] = 0
    cv2.imwrite("blackwhite.jpg",image)
    return image

    # END OF FUNCTION.

def averageTwoImages(image1, image2):
    """ This function averages the pixels of the two input images.

    Assignment Instructions: Obtain the average image by adding up the two input
    images on a per pixel basis and dividing them by two.

    You may use any / all functions to obtain the average image output.

    Note: You may assume image1 and image2 are the SAME size.

    Args:
        image1 (numpy.ndarray): A grayscale image represented in a numpy array.
        image2 (numpy.ndarray): A grayscale image represented in a numpy array.

    Returns:
        numpy.ndarray: The average of image1 and image2.

    """
    # WRITE YOUR CODE HERE.
    rows = len(image1)
    columns = len(image1[0])
    #average = np.empty([rows,columns],dtype=int)
    average = np.zeros((rows,columns),dtype=np.uint8)
    for i in range(rows):
        for j in range(columns):
            average[i][j] = (int(image1[i][j]) + int(image2[i][j]))/2
    cv2.imwrite("average.jpg",average)
    return average
    # END OF FUNCTION.

def flipHorizontal(image):
    """ This function flips the input image across the horizontal axis.

    Assignment Instructions: Given an input image, flip the image on the
    horizontal axis. This can be interpreted as switching the first and last
    column of the image, the second and second to last column, and so on.

    You may use any / all functions to flip the image horizontally.

    Args:
        image (numpy.ndarray): A grayscale image represented in a numpy array.

    Returns:
        numpy.ndarray: The horizontally flipped image.

    """
    # WRITE YOUR CODE HERE.
    rows = len(image)
    columns = len(image[0])
    result = np.empty([rows,columns],dtype = np.uint8)
    for i in range(rows):
        for j in range(columns):
            target = image[i][j]
            result[i][columns-j-1] = target
    cv2.imwrite("flip.jpg",result)
    return result
    # END OF FUNCTION.