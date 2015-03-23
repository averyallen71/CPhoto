# ASSIGNMENT 8
# Robert Avery Allen

import numpy as np
import scipy as sp
import scipy.signal
import cv2

# Import ORB as SIFT to avoid confusion.
try:
    from cv2 import ORB as SIFT
except ImportError:
    try:
        from cv2 import SIFT
    except ImportError:
        try:
            SIFT = cv2.ORB_create
        except:
            raise AttributeError("Your OpenCV(%s) doesn't have SIFT / ORB."
                                 % cv2.__version__)


""" Assignment 8 - Panoramas

This file has a number of functions that you need to fill out in order to
complete the assignment. Please write the appropriate code, following the
instructions on which functions you may or may not use.

GENERAL RULES:
    1. DO NOT INCLUDE code that saves, shows, displays, writes the image that
    you are being passed in. Do that on your own if you need to save the images
    but the functions should NOT save the image to file. (This is a problem
    for us when grading because running 200 files results a lot of images being
    saved to file and opened in dialogs, which is not ideal). Thanks.

    2. DO NOT import any other libraries aside from the three libraries that we
    provide. You may not import anything else, you should be able to complete
    the assignment with the given libraries (and in most cases without them).

    3. DO NOT change the format of this file. Do not put functions into classes,
    or your own infrastructure. This makes grading very difficult for us. Please
    only write code in the allotted region.
"""

def getImageCorners(image):
    """ For an input image, return its four corners.

    You should be able to do this correctly without instruction. If in doubt,
    resort to the testing framework. The order in which you store the corners
    does not matter.

    Note: The reasoning for the shape of the array can be explained if you look
    at the documentation for cv2.perspectiveTransform which we will use on the
    output of this function. Since we will apply the homography to the corners
    of the image, it needs to be in that format.

    Another note: When storing your corners, they are assumed to be in the form
    (X, Y) -- keep this in mind and make SURE you get it right.

    Args:
        image (numpy.ndarray): Input can be a grayscale or color image.

    Returns:
        corners (numpy.ndarray): Array of shape (4, 1, 2). Type of values in the
                                 array is np.float32.
    """
    corners = np.zeros((4, 1, 2), dtype=np.float32)
    # WRITE YOUR CODE HERE
    top_left = [0,0]
    bottom_left = [0,len(image)]
    top_right = [len(image[0]),0]
    bottom_right = [len(image[0]),len(image)]

    corners[0] = [top_left[0], top_left[1]]
    corners[1] = [top_right[0], top_right[1]]
    corners[2] = [bottom_left[0], bottom_left[1]]
    corners[3] = [bottom_right[0], bottom_right[1]]
    
    return corners
    # END OF FUNCTION

def findMatchesBetweenImages(image_1, image_2, num_matches):
    """ Return the top list of matches between two input images.

    Note: You will not be graded for this function. This function is almost
    identical to the function in Assignment 7 (we just parametrized the number
    of matches). We expect you to use the function you wrote in A7 here. We will
    also release a solution for how to do this after A7 submission has closed.

    If your code from A7 was wrong, don't worry, you will not lose points in
    this assignment because your A7 code was wrong (hence why we will provide a
    solution for you after A7 closes).

    This function detects and computes SIFT (or ORB) from the input images, and
    returns the best matches using the normalized Hamming Distance through brute
    force matching.

    Args:
        image_1 (numpy.ndarray): The first image (grayscale).
        image_2 (numpy.ndarray): The second image. (grayscale).
        num_matches (int): The number of desired matches. If there are not
                           enough, return as many matches as you can.

    Returns:
        image_1_kp (list): The image_1 keypoints, the elements are of type
                           cv2.KeyPoint.
        image_2_kp (list): The image_2 keypoints, the elements are of type 
                           cv2.KeyPoint.
        matches (list): A list of matches, length 'num_matches'. Each item in 
                        the list is of type cv2.DMatch. If there are less 
                        matches than num_matches, this function will return as
                        many as it can.

    """
    # matches - type: list of cv2.DMath
    matches = None
    # image_1_kp - type: list of cv2.KeyPoint items.
    image_1_kp = None
    # image_1_desc - type: numpy.ndarray of numpy.uint8 values.
    image_1_desc = None
    # image_2_kp - type: list of cv2.KeyPoint items.
    image_2_kp = None
    # image_2_desc - type: numpy.ndarray of numpy.uint8 values.
    image_2_desc = None

    # COPY YOUR CODE FROM A7 HERE.
    sift = SIFT()
    image_1_kp, image_1_desc = sift.detectAndCompute(image_1,None)
    image_2_kp, image_2_desc = sift.detectAndCompute(image_2,None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(image_1_desc,image_2_desc)
    matches = sorted(matches, key = lambda x:x.distance)
    matches = matches[:10]

    return image_1_kp, image_2_kp, matches
  # END OF FUNCTION.

def findHomography(image_1_kp, image_2_kp, matches):
    """ Returns the homography between the keypoints of image 1, image 2, and
        its matches.

    Follow these steps:
        1. Iterate through matches and:
            1a. Get the x, y location of the keypoint for each match. Look up
                the documentation for cv2.DMatch. Image 1 is your query image,
                and Image 2 is your train image. Therefore, to find the correct
                x, y location, you index into image_1_kp using match.queryIdx,
                and index into image_2_kp using match.trainIdx. The x, y point
                is stored in each keypoint (look up documentation).
            1b. Set the keypoint 'pt' to image_1_points and image_2_points, it
                should look similar to this inside your loop:
                    image_1_points[match_idx] = image_1_kp[match.queryIdx].pt
                    # Do the same for image_2 points.

        2. Call cv2.findHomography and pass in image_1_points, image_2_points,
           use method=cv2.RANSAC and ransacReprojThreshold=5.0. I recommend
           you look up the documentation on cv2.findHomography to better
           understand what these parameters mean.
        3. cv2.findHomography returns two values, the homography and a mask.
           Ignore the mask, and simply return the homography.

    Args:
        image_1_kp (list): The image_1 keypoints, the elements are of type
                           cv2.KeyPoint.
        image_2_kp (list): The image_2 keypoints, the elements are of type 
                           cv2.KeyPoint.
        matches (list): A list of matches. Each item in the list is of type
                        cv2.DMatch.
    Returns:
        homography (numpy.ndarray): A 3x3 homography matrix. Each item in
                                    the matrix is of type numpy.float64.
    """
    image_1_points = np.zeros((len(matches), 1, 2), dtype=np.float32)
    image_2_points = np.zeros((len(matches), 1, 2), dtype=np.float32)

    # WRITE YOUR CODE HERE.
    for idx in range(len(matches)):
        match = matches[idx]
        image_1_points[idx] = image_1_kp[match.queryIdx].pt
        image_2_points[idx] = image_2_kp[match.trainIdx].pt

    
    # Replace this return statement with the homography.
    return cv2.findHomography(image_1_points,image_2_points,method=cv2.RANSAC,ransacReprojThreshold=5.0)[0]
    # END OF FUNCTION

def blendImagePair(warped_image, image_2, point):
    """ This is the blending function. We provide a basic implementation of
    this function that we would like you to replace.

    This function takes in an image that has been warped and an image that needs
    to be inserted into the warped image. Lastly, it takes in a point where the
    new image will be inserted.

    The current method we provide is very simple, it pastes in the image at the
    point. We want you to replace this and blend between the images.

    We want you to be creative. The most common implementation would be to take
    the average between image 1 and image 2 only for the pixels that overlap.
    That is just a starting point / suggestion but you are encouraged to use
    other approaches.

    Args:
        warped_image (numpy.ndarray): The image provided by cv2.warpPerspective.
        image_2 (numpy.ndarray): The image to insert into the warped image.
        point (numpy.ndarray): The point (x, y) to insert the image at.

    Returns:
        image: The warped image with image_2 blended into it.
    """
    output_image = np.copy(warped_image)
    # REPLACE THIS WITH YOUR BLENDING CODE.
    output_image[point[1]:point[1] + image_2.shape[0],
                 point[0]:point[0] + image_2.shape[1]] = image_2
    for i in range(len(image_2)):
        for j in range(len(image_2[0])):
            im2_point = image_2[i][j]
            warped_point = warped_image[i + point[1], j + point[0]]

            if warped_point[0] < 15 and warped_point[1] < 15 and warped_point[2] <15:
                output_image[i + point[1], j + point[0]] = im2_point
            else:
                weight = (len(image_2[0])/2.0 + j) / len(image_2[0])
                if weight > 1:
                    weight = 1
                counter = 1 - weight   
                outputPoint = [float(im2_point[0]) * weight + float(warped_point[0]) * counter, float(im2_point[1]) * weight + float(warped_point[1]) * counter, float(im2_point[2]) * weight + float(warped_point[2]) * counter]
                output_image[i + point[1], j + point[0]] = outputPoint
    cv2.imwrite("warped.jpg", warped_image)
    cv2.imwrite("image2.jpg",image_2)
    cv2.imwrite("output.jpg",output_image)
    return output_image
    # END OF FUNCTION

def warpImagePair(image_1, image_2, homography):
    """ Warps image 1 so it can be blended with image 2 (stitched).

    Follow these steps:
        1. Obtain the corners for image 1 and image 2 using the function you
        wrote above.
        
        2. Transform the perspective of the corners of image 1 by using the
        image_1_corners and the homography to obtain the transformed corners.
        
        Note: Now we know the corners of image 1 and image 2. Out of these 8
        points (the transformed corners of image 1 and the corners of image 2),
        we want to find the minimum x, maximum x, minimum y, and maximum y. We
        will need this when warping the perspective of image 1.

        3. Join the two corner arrays together (the transformed image 1 corners,
        and the image 2 corners) into one array of size (8, 1, 2).

        4. For the first column of this array, find the min and max. This will
        be your minimum and maximum X values. Store into x_min, x_max.

        5. For the second column of this array, find the min and max. This will
        be your minimum and maximum Y values. Store into y_min, y_max.

        6. Create a translation matrix that will shift the image by the required
        x_min and y_min (should be a numpy.ndarray). This looks like this:
            [[1, 0, -1 * x_min],
             [0, 1, -1 * y_min],
             [0, 0, 1]]

        Note: We'd like you to explain the reasoning behind multiplying the
        x_min and y_min by negative 1 in your writeup.

        7. Compute the dot product of your translation matrix and the homography
        in order to obtain the homography matrix with a translation.

        8. Then call cv2.warpPerspective. Pass in image 1, the dot product of
        the matrix computed in step 6 and the passed in homography and a vector
        that will fit both images, since you have the corners and their max and
        min, you can calculate it as (x_max - x_min, y_max - y_min).

        9. To finish, you need to blend both images. We have coded the call to
        the blend function for you.

    Args:
        image_1 (numpy.ndarray): Left image.
        image_2 (numpy.ndarray): Right image.
        homography (numpy.ndarray): 3x3 matrix that represents the homography
                                    from image 1 to image 2.

    Returns:
        output_image (numpy.ndarray): The stitched images.
    """
    # Store the result of cv2.warpPerspective in this variable.
    warped_image = None
    # The minimum and maximum values of your corners.
    x_min = 0
    y_min = 0
    x_max = 0
    y_max = 0

    # WRITE YOUR CODE HERE
    image_1_corners = getImageCorners(image_1)
    image_2_corners = getImageCorners(image_2)
    
    transformed = cv2.perspectiveTransform(image_1_corners,homography)
    corners = [transformed[0],transformed[1],transformed[2],transformed[3],image_2_corners[0],
        image_2_corners[1],image_2_corners[2],image_2_corners[3]]

    y_min = corners[0][0][1]
    x_min = corners[0][0][0]
    y_max = corners[0][0][1]
    x_max = corners[0][0][0]

    for idx in range(len(corners)):
        xVal = corners[idx][0][0]
        yVal = corners[idx][0][1]

        if xVal > x_max:
            x_max = xVal
        if xVal < x_min:
            x_min = xVal
        if yVal > y_max:
            y_max = yVal
        if yVal < y_min:
            y_min = yVal

    translation = np.array([[1, 0, -1 * x_min],[0, 1, -1 * y_min],[0, 0, 1]])

    dotProd = np.dot(translation,homography)

    warped_image = cv2.warpPerspective(image_1,dotProd,(x_max - x_min, y_max - y_min))
    # END OF CODING
    output_image = blendImagePair(warped_image, image_2,
                                  (-1 * x_min, -1 * y_min))
    return output_image

# Some simple testing.
# image_1 = cv2.imread("images/source/panorama_1/1.jpg")
# image_2 = cv2.imread("images/source/panorama_1/2.jpg")
# image_1_kp, image_2_kp, matches = findMatchesBetweenImages(image_1, image_2,
#                                                            20)
# homography = findHomography(image_1_kp, image_2_kp, matches)
# result = warpImagePair(image_1, image_2, homography)
# cv2.imwrite("images/output/panorama_1_result.jpg", result)