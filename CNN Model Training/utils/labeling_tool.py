import cv2 as cv
import numpy as np
import os
import shutil
from pathlib import Path
import corner_selctor 
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
# Checks if the warped image looks valid by sampling the center region.
# If the center is mostly black, the warp failed.
def is_warp_valid(warped):
    # Grab the center 100x100 region of the warped board
    center = warped[150:250, 150:250]
    
    # Calculate average brightness
    avg_brightness = np.mean(center)
    
    # If average brightness is very low, warp is probably wrong
    return avg_brightness > 30 

def cut_into_squares(board_images):
    squares = []
    files = "abcdefgh"
    i = 0
    #  go throuth the images 
    while True:
        if i >= len(board_images):
            break
        img_name = os.path.basename(board_images[i])
        img_name = os.path.splitext(img_name)[0]  # remove .png extension

        image = cv.imread(board_images[i])
        

        # Check if the corners were already selected
        corners = corner_selctor.load_or_select_corners(image, board_images[i])
        image = cv.resize(image, (1920, 1080))
        warped = warp_board(image, corners)

        # Check to see if the corners were selected correctly
        if not is_warp_valid(warped):
            corner_selctor.delete_corners(board_images[i])
            continue
        i += 1
        # Then cut image into squares
        for row in range(8):
            rank = str(8- row)

            for col in range(8):
                file_letter = files[col]
                square_name = files[col] + rank

                # Calculate the top-left corner of this square
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE

                # Add overlap padding, clamped to image boundaries
                x1 = max(0, x - OVERLAP)
                y1 = max(0, y - OVERLAP)
                x2 = min(WARP_SIZE, x + SQUARE_SIZE + OVERLAP)
                y2 = min(WARP_SIZE, y + SQUARE_SIZE + OVERLAP)

                # Cut the square out of the warped image
                square = warped[y1:y2, x1:x2]
                
                # Keep track of which square this is
                squares.append({
                    "image": square,
                    "row": row,
                    "col": col,
                    "name": img_name + "_" + square_name  # e.g. "a8", "b7" etc
                })
    
    return squares


