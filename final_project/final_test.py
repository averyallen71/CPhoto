import cv2
import unittest

from encode import colorToBinaryString
from encode import recreateColorImage
from encode import convertToBlackAndWhite
from encode import numberOfPixels
from encode import encode
from encode import decode


if __name__ == '__main__':

    guest = cv2.imread("test_image.jpg",3)
    host  = cv2.imread("test_image2.jpg")
    encoded = encode(host,guest)
    cv2.imwrite("encoded.jpg",encoded)
    cv2.imwrite("decoded.jpg",decode(encoded))

   