import cv2
import unittest
import Tkinter

from encode import colorToBinaryString
from encode import greyscaleToBinaryString
from encode import recreateColorImage
from encode import recreateGreyscaleImage
from encode import convertToBlackAndWhite
from encode import encode
from encode import decode
from encode import bitsRequired
from encode import recoverBits
from encode import availableBitCount
from gaussian_pyramid import gaussPyramid


if __name__ == '__main__':
	guest = cv2.imread("guest.jpg",3)
	pyr = gaussPyramid(guest,2)
	cv2.imwrite("pyr1.jpg",pyr[0])
	cv2.imwrite("pyr2.jpg",pyr[1])
	cv2.imwrite("pyr3.jpg",pyr[2])
	
	print "*****************************DONE 1********************************"
	'''
	host = cv2.imread("host.jpg",3)
	for i in range(len(encodedOrig)):
		for j in range(len(encodedOrig[0])):
			r1 = encodedOrig[i][j][0]
			r2 = host[i][j][0]

			g1 = encodedOrig[i][j][1]
			g2 = host[i][j][1]

			b1 = encodedOrig[i][j][2]
			b2 = host[i][j][2]

			if r1 != r2 or g1 != g2 or b1 != b2:
				print "HERE"
				print str(r1) + " " + str(r2)

				break
	'''

	'''
	print recoverBits(encoded)[:24]
	cv2.imwrite("encode.jpg",encoded)
	print recoverBits(encoded)[:24]
	encoded = cv2.imread("encode.jpg",3)
	print recoverBits(encoded)[:24]
	cv2.imwrite("decode.jpg",decode(encoded))
	'''
	
	
