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

def colorToBinaryString(image):
    
    bits = ""
    rows = bin(len(image))[2:]
    cols = bin(len(image[0]))[2:]
    rows = rows.zfill(12)
    cols = cols.zfill(12)
    bits += rows
    bits += cols

    for i in range(len(image)):
        for j in range(len(image[1])):
            bits += bin(image[i][j][0])[2:].zfill(8)
            bits += bin(image[i][j][1])[2:].zfill(8)
            bits += bin(image[i][j][2])[2:].zfill(8)

    return bits

def recreateColorImage(bits):
    rows = int(bits[0:12],2)
    cols = int(bits[12:24],2)
    blank_image = np.zeros((rows,cols,3), np.uint8)
    bitIndex = 24
    for i in range(rows):
        for j in range(cols):

            redBin = bits[bitIndex:bitIndex+8]
            if redBin:
                redChannel = int(redBin,2)
                bitIndex+=8
            
            greenBin = bits[bitIndex:bitIndex+8]
            if greenBin:
                greenChannel = int(greenBin,2)
                bitIndex+=8

            blueBin = bits[bitIndex:bitIndex+8]
            if blueBin:
                blueChannel = int(blueBin,2)
                bitIndex+=8

            blank_image[i][j][0] = redChannel
            blank_image[i][j][1] = greenChannel
            blank_image[i][j][2] = blueChannel

    return blank_image

def encode(host,guest):
    guestBits = colorToBinaryString(guest)

    rows = len(host)
    cols = len(host[0])
    bitIndex = 0
    for i in range(rows):
        for j in range(cols):
            red = host[i][j][0]
            green = host[i][j][1]
            blue = host[i][j][2]

            redBin = bin(red)[2:].zfill(8)[:6]
            greenBin = bin(green)[2:].zfill(8)[:6]         
            blueBin = bin(blue)[2:].zfill(8)[:6]
            

            if bitIndex+2 < len(guestBits):
                redBin += guestBits[bitIndex:bitIndex+2]
                bitIndex +=2
            else:
                break
            
            if bitIndex+2 < len(guestBits):
                greenBin += guestBits[bitIndex:bitIndex+2]
                bitIndex +=2
            else:
                break
            
            if bitIndex+2 < len(guestBits):
                blueBin += guestBits[bitIndex:bitIndex+2]
                bitIndex +=2
            else:
                break

            host[i][j][0] = int(redBin,2)
            host[i][j][1] = int(greenBin,2)
            host[i][j][2] = int(blueBin,2)

    
    return host


def recoverBits(pic):
    
    rows = len(pic)
    cols = len(pic[0])
    bits = ""
    for i in range(rows):
        for j in range(cols):
            bits += bin(pic[i][j][0])[2:].zfill(8)[-2:]
            bits += bin(pic[i][j][1])[2:].zfill(8)[-2:]
            bits += bin(pic[i][j][2])[2:].zfill(8)[-2:]
    return bits


def decode(pic):
    bits = recoverBits(pic)
    return(recreateColorImage(bits))
    
