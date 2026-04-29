import cv2 as cv
import numpy as np
import random
import os
import shutil
from pathlib import Path
from augmentaion import augment_class
import corner_selector 
import json


IMAGE_FOLDER = "data/raw"
OUTPUT_FOLDER = "data/squares"
LABEL_FILE = "data/square_labels.json"

WARP_SIZE = 400 # After homography the board becomes a 400×400 image
SQUARE_SIZE = WARP_SIZE // 8 # Each square will be about 50x50 pictures
OVERLAP = 8 # How much each image will bleed into other neighboring squares

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
    #  go through the images 
    while True:
        if i >= len(board_images):
            break
        img_name = os.path.basename(board_images[i])
        img_name = os.path.splitext(img_name)[0]  # remove .png extension

        image = cv.imread(board_images[i])
        

        # Check if the corners were already selected
        corners = corner_selector.load_or_select_corners(image, board_images[i])
        image = cv.resize(image, (1920, 1080))
        warped = warp_board(image, corners)

        # Check to see if the corners were selected correctly
        if not is_warp_valid(warped):
            corner_selector.delete_corners(board_images[i])
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


def labeling_tool(square):

    KEY_MAP = {
        ord('e'): "empty",
        ord('p'): "white_pawn",
        ord('P'): "black_pawn",
        ord('n'): "white_knight",
        ord('N'): "black_knight",
        ord('b'): "white_bishop",
        ord('B'): "black_bishop",
        ord('r'): "white_rook",
        ord('R'): "black_rook",
        ord('q'): "white_queen",
        ord('Q'): "black_queen",
        ord('k'): "white_king",
        ord('K'): "black_king",
    }

    # Check if already labeled before showing anything
    if os.path.exists(LABEL_FILE):
        with open(LABEL_FILE, 'r') as f:
            all_squares = json.load(f)
        if square["name"] in all_squares:
            return  # skip immediately, no popup

    display = cv.resize(square["image"], (300, 300))
    instruction = "Type the corresponding letter of this piece(Black Uppercase, White Lowercase)"

    cv.imshow("Label Square", display)
    cv.putText(display, instruction, (20, 40),
                    cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
    while True:
        key = cv.waitKey(0)

        if key == 27:  # ESC
            print("Quitting!")
            cv.destroyAllWindows()
            return
        
        elif key == ord('s'):  # skip
            break

        elif key in KEY_MAP:
            label = KEY_MAP[key]
            save_square(square, label)
            break
        
        else:
            print("Invalid key, try again")
            # Loop continues, waiting for valid key


def save_square(square, label):

    if os.path.exists(LABEL_FILE):
        with open(LABEL_FILE, 'r') as f:
            # Grab every square that we have saved
            all_squares = json.load(f)
    else:
            all_squares = {}

    # We already have this square saved
    if square["name"] in all_squares:
        return
    # save the image of the square
    filename = os.path.join(OUTPUT_FOLDER, square["name"] + ".png")
    cv.imwrite(filename, square["image"])

    all_squares[square["name"]] = label

    with open(LABEL_FILE, 'w') as f:
        json.dump(all_squares, f, indent=4)

# Split the data into the right folders for testing
def split_data():

    # Load the labels
    if not os.path.exists(LABEL_FILE):
        print("No label file found!")
        return
    
    with open(LABEL_FILE, 'r') as f:
        labels = json.load(f)

    # Shuffle for randomness
    items = list(labels.items())
    random.shuffle(items)

    # Calculate split sizes
    n_train = int(len(items) * TRAIN_RATIO)
    n_val = int(len(items) * VAL_RATIO)

    splits = {
        "train": items[:n_train],
        "val":   items[n_train:n_train + n_val],
        "test":  items[n_train + n_val:]
    }

    moved = 0

    for split, squares in splits.items():
        for name, label in squares:
            src = os.path.join(OUTPUT_FOLDER, name + ".png")
            dst_folder = os.path.join(OUTPUT_FOLDER, split, label)
            dst = os.path.join(dst_folder, name + ".png")

            os.makedirs(dst_folder, exist_ok=True)

            if os.path.exists(src):
                shutil.move(src, dst)
                moved += 1
    
    print("Done")
    print("Moved: " + str(moved))


def check_labels():
    squares = cut_into_squares(board_images)
    for square in squares:
        labeling_tool(square)
    # Split the data into folders and subfolders
    split_data()
    # Augment the data
    splits_dict = {
        "train": 200, # Have at least 200 photos for each category
        "test": 20, # Have at least 20 photos for each category
        "val": 20 # Have at least 20 photos for each category
    }

    for split, target_count in splits_dict.items():
        split_folder = os.path.join("data/squares", split)
        for class_name in os.listdir(split_folder):
            class_folder = os.path.join(split_folder, class_name)
            augment_class(class_folder, target_count)

check_labels()