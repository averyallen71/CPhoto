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
    
    rows = int(bits[5:17],2)
    cols = int(bits[17:29],2)
    blank_image = np.zeros((rows,cols,3), np.uint8)
    bitIndex = 29
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
    rows = int(bits[5:17],2)
    cols = int(bits[17:29],2)
    blank_image = np.zeros((rows,cols), np.uint8)
    bitIndex = 29
    for i in range(rows):
        for j in range(cols):

            intensityBin = bits[bitIndex:bitIndex+8]
            if intensityBin:
                intensity = int(intensityBin,2)
                blank_image[i][j] = intensity
                bitIndex+=8

    return blank_image

'''
options string:
                 (1) (2)(3)
                XXX  X  X 
    1 - bits to use
    2 - greyscaleToBinaryStringscale
    3 - placeholder
'''
def encode(host,guest,options):
    if options[3] == '1':
        grey = cv2.cvtColor(guest, cv2.COLOR_RGB2GRAY)
        guestBits =  greyscaleToBinaryString(grey,options)
    else:
        guestBits = colorToBinaryString(guest,options)

    rows = len(host)
    cols = len(host[0])
    bPerPix = int(options[:3],2)



    #Amount of bits stored per pixel must be stored in a set position in first pixel
    red = host[0][0][0]
    green = host[0][0][1]
    blue = host[0][0][2]

    redBin = bin(red)[2:].zfill(8)[:7] + options[0]
    greenBin = bin(green)[2:].zfill(8)[:7] + options[1]     
    blueBin = bin(blue)[2:].zfill(8)[:7] + options[2]

    host[0][0][0] = int(redBin,2)
    host[0][0][1] = int(greenBin,2)
    host[0][0][2] = int(blueBin,2)

    bitIndex = 3
    for i in range(rows):
        for j in range(cols):
            if i is 0 and j is 0:
                continue
            
            red = host[i][j][0]
            green = host[i][j][1]
            blue = host[i][j][2]

            redBin = bin(red)[2:].zfill(8)[:8-bPerPix]
            greenBin = bin(green)[2:].zfill(8)[:8-bPerPix]         
            blueBin = bin(blue)[2:].zfill(8)[:8-bPerPix]
            

            if bitIndex+bPerPix < len(guestBits):
                redBin += guestBits[bitIndex:bitIndex+bPerPix]
                bitIndex +=bPerPix
            else:
                break
            
            if bitIndex+bPerPix < len(guestBits):
                greenBin += guestBits[bitIndex:bitIndex+bPerPix]
                bitIndex +=bPerPix
            else:
                break
            
            if bitIndex+bPerPix < len(guestBits):
                blueBin += guestBits[bitIndex:bitIndex+bPerPix]
                bitIndex +=bPerPix
            else:
                break

            host[i][j][0] = int(redBin,2)
            host[i][j][1] = int(greenBin,2)
            host[i][j][2] = int(blueBin,2)
            
    
    return host

def recoverBits(image):
    
    rows = len(image)
    cols = len(image[0])

    #Get bit per pixels information stored in first pixel
    bits = ""
    bits += bin(image[0][0][0])[2:].zfill(8)[-1:]
    bits += bin(image[0][0][1])[2:].zfill(8)[-1:]
    bits += bin(image[0][0][2])[2:].zfill(8)[-1:]

    bPerPix = int(bits,2)
    for i in range(rows):
        for j in range(cols):
            if i is 0 and j is 0:
                continue
            bits += bin(image[i][j][0])[2:].zfill(8)[-bPerPix:]
            bits += bin(image[i][j][1])[2:].zfill(8)[-bPerPix:]
            bits += bin(image[i][j][2])[2:].zfill(8)[-bPerPix:]
    return bits

def decode(image):
    bits = recoverBits(image)
    options = bits[:5]
    if options[3] == '1':
        return(recreateGreyscaleImage(bits))
    else:
        return(recreateColorImage(bits))
    
def availableBitCount(image,bitsPerChannel):
    # the -1 and + 3 are because of predetermined bit location for storing 
    # bits used per pixel
    return (len(image)*len(image[0]) - 1)*3 * bitsPerChannel + 3


def bitsRequired(image,options):
    bits = len(image)*len(image[0]) * 8 * 3 
    if options[3] == '1':
        bits /= 3
    return bits + len(options) + 24 