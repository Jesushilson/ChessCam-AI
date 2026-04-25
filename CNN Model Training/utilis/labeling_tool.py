import cv2 as cv
import numpy as np
import os
import shutil
from pathlib import Path
import json


IMAGE_FOLDER = "data/raw"
OUTPUT_FOLDER = "data/squares"

WARP_SIZE = 400 # After homography the board becomes a 400×400 image
SQUARE_SIZE = WARP_SIZE // 8 # Each square will be about 50x50 pictures
OVERLAP = 8 # How much each image will bleed into other neigboring squares

TRAIN_RATIO = 0.8
VAL_RATIO = 0.1

# Grab a list of all the images
board_images = os.listdir(IMAGE_FOLDER)

# Find the corners of the chess board
def detect_corners(image):
    # Contour based detection:

    # Convert image to Grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # Add a gaussain blur to the image
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    # Find the edges of the smoothed image
    edges = cv.Canny(blurred, 50, 150)

    # find contours, focusing the outer/stronger contours
    contours = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Sort from largest to smallest since the board is the biggest in the image
    contours = sorted(contours, key=cv.contourArea, reverse=True)


    # Now we serach for a rectangle in our contours
    for contour in contours[:5]:
        # Calculate the perimeter of the contour
        perimeter = cv.arcLength(contour, True)
        # Simplifying the contour shape by removing excess points on the perimiter
        approx = cv.approxPolyDP(contour, 0.2 * perimeter, True)

        # There are 4 corners/points
        if len(approx) == 4:
            # Calculate the area of the contour
            area = cv.contourArea(approx)

            # Check if the area is bigger than 20% of our image
            if area > (image.shape[0] * image.shape[1] * 0.2):
                # Likely to be our Chess Board
                
                # Clean up the formatting
                corners = approx.reshape(4, 2).astype(np.float32)
                return order_corners(corners)

    # Unable to find the right shape 
    return None

# helper function to Order the corners to always have a set order for the homography
def order_corners(corners):
    # Calculate the center of the board 
    center = corners.mean(axis=0)
    # Create an empty array to hold our ordered 
    ordered = np.zeros((4,2), dtype=np.float32)

    # Go through each corner and calculate which slot it goes to based on the center
    for pt in corners:
        if pt[0] < center[0] and pt[1] < center[1]:
            ordered[0] = pt  # top-left
        elif pt[0] > center[0] and pt[1] < center[1]:
            ordered[1] = pt  # top-right
        elif pt[0] < center[0] and pt[1] > center[1]:
            ordered[2] = pt  # bottom-left
        else:
            ordered[3] = pt  # bottom-right

    return ordered

# Here we can warp the image so it fits in a 400x400 radius where
# Where all the corners will match 
def warp_board(image, corners):
    # Where each corner should matcch up
    desination_img = np.float32([
        [0,0],
        [WARP_SIZE],
        [0, WARP_SIZE],
        [WARP_SIZE, WARP_SIZE]
    ])
    
    # Retrieves the matrix that descirbes how each corner needs to be stretched to fit in desination_img 
    matrix = cv.getPerspectiveTransform(corners, desination_img)

    # Applies the math to every pixel to actually fit that size
    warped = cv.warpPerspective(image, matrix, WARP_SIZE, WARP_SIZE)


