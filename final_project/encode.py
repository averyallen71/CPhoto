import cv2
import numpy as np
import scipy as sp

def convertToBlackAndWhite(image):
    """ 
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

def colorToBinaryString(image, options):
    
    bits = options
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

def greyscaleToBinaryString(image,options):

    bits = options
    rows = bin(len(image))[2:]
    cols = bin(len(image[0]))[2:]
    rows = rows.zfill(12)
    cols = cols.zfill(12)
    bits += rows
    bits += cols

    for i in range(len(image)):
        for j in range(len(image[0])):
            bits += bin(image[i][j])[2:].zfill(8)
    return bits

def recreateColorImage(bits):
    
    rows = int(bits[2:14],2)
    cols = int(bits[14:26],2)
    blank_image = np.zeros((rows,cols,3), np.uint8)
    bitIndex = 26
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

def recreateGreyscaleImage(bits):
    rows = int(bits[2:14],2)
    cols = int(bits[14:26],2)
    blank_image = np.zeros((rows,cols), np.uint8)
    bitIndex = 26
    for i in range(rows):
        for j in range(cols):

            intensityBin = bits[bitIndex:bitIndex+8]
            if intensityBin:
                intensity = int(intensityBin,2)
                blank_image[i][j] = intensity
                bitIndex+=8

    return blank_image

def encode(host,guest,options):
    if options[0] == '1':
        grey = cv2.cvtColor(guest, cv2.COLOR_RGB2GRAY)
        guestBits =  greyscaleToBinaryString(grey,options)
    else:
        guestBits = colorToBinaryString(guest,options)

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

def recoverBits(image):
    
    rows = len(image)
    cols = len(image[0])
    bits = ""
    for i in range(rows):
        for j in range(cols):
            bits += bin(image[i][j][0])[2:].zfill(8)[-2:]
            bits += bin(image[i][j][1])[2:].zfill(8)[-2:]
            bits += bin(image[i][j][2])[2:].zfill(8)[-2:]
    return bits

def decode(image):
    bits = recoverBits(image)
    options = bits[:2]
    if options[0] == '1':
        return(recreateGreyscaleImage(bits))
    else:
        return(recreateColorImage(bits))
    
def availableBitCount(image):
    return len(image)*len(image[0])*6

def bitsRequired(image,options):
    bits = len(image)*len(image[0]) * 8 * 3
    if options[0] == '1':
        bits /= 3
    return bits + len(options) + 24