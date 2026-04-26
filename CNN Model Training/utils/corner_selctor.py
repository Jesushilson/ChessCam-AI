import cv2 as cv
import numpy as np
import os
import shutil
from pathlib import Path
import json

# File that will only be used for training
CORNERS_FILE = "utils/corners.json"

# Function to help with training the images
# It will allow me to select the corners of each image
def manual_corner_selection(image):
    # Will hold the coordinates of the corners 
    corners = []
    display = image.copy()
    labels = ["Click the TOP LEFT corner", "Click the TOP RIGHT corner",
              "Click Bottom Left corner", "Click the BOTTOM RIGHT corner "]
    

    def mouse_callback(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            corners.append([x, y])
            cv.circle(display, (x, y), 6, (0, 255, 0), -1)
            cv.imshow("Select Corners", display)
    
    cv.namedWindow("Select Corners", cv.WINDOW_NORMAL)
    cv.setMouseCallback("Select Corners", mouse_callback)

    while len(corners) < 4:
        img_copy = display.copy()
        # Show the right instruction based on what is left
        instruction = labels[len(corners)]
        cv.putText(img_copy, instruction, (20, 40),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
        # display the image
        cv.imshow("Select Corners", img_copy)
        cv.waitKey(1)

    cv.destroyWindow("Select Corners")
    return np.float32(corners)

# Check if we have saved the corner details yet
def load_or_select_corners(image, img_path):
    img_name = os.path.basename(img_path)
    if os.path.exists(CORNERS_FILE):
        with open(CORNERS_FILE, 'r') as f:
            # Grab every corner that we have saved
            all_corners = json.load(f)
    else:
            all_corners = {}

    # Check if we have this image's corners saved
    if img_name in all_corners:
        return np.float32(all_corners[img_name])

    # Image corners not saved
    corners = manual_corner_selection(image)

    all_corners[img_name] = corners.tolist()

    with open(CORNERS_FILE, 'w') as f:
        json.dump(all_corners, f, indent=4)
        print("Corners saved for next time!")

    return corners