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
board_images = [
    os.path.join(IMAGE_FOLDER, f) 
    for f in os.listdir(IMAGE_FOLDER) 
    if f.endswith('.png') or f.endswith('.jpg')
]


# Here we can warp the image so it fits in a 400x400 radius where
# Where all the corners will match 
def warp_board(image, corners):
    # Where each corner should matcch up
    desination_img = np.float32([
        [0,0],
        [WARP_SIZE, 0],
        [0, WARP_SIZE],
        [WARP_SIZE, WARP_SIZE]
    ])
    
    # Retrieves the matrix that descirbes how each corner needs to be stretched to fit in desination_img 
    matrix = cv.getPerspectiveTransform(corners, desination_img)

    # Applies the math to every pixel to actually fit that size
    warped = cv.warpPerspective(image, matrix, (WARP_SIZE, WARP_SIZE))

    return warped

image = cv.imread(board_images[25])
image = cv.resize(image, (800, 600))
# cv.imshow("test Board", image)
# cv.waitKey(0)  # press any key to continue
# cv.destroyWindow("test Board")





