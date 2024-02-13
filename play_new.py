"""Game of tic tac toe using OpenCV to play against computer"""

import os
import sys
import cv2
import argparse
import numpy as np

from keras.models import load_model

from data.utils import auto_corner_detection
from data.utils import detections


def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--image_path", help="path to image file")

    parser.add_argument('--model', '-m', type=str, default='data/model.h5',
                        help='model file (.h5) to detect Xs and Os')

    return parser.parse_args()


# def find_sheet_paper(frame, thresh, add_margin=True):
def find_sheet_paper(frame):
    """Detect the coords of the sheet of paper the game will be played on"""
    # stats = detections.find_corners(thresh)
    # # First point is center of coordinate system, so ignore it
    # # We only want sheet of paper's corners
    # corners = stats[1:, :2]
    # corners = imutilis.order_points(corners)
    # # Get bird view of sheet of paper
    # paper = imutilis.four_point_transform(frame, corners)
    # if add_margin:
    #     paper = paper[10:-10, 10:-10]
    # return paper, corners
    #
    paper = auto_corner_detection.auto_corner(frame)
    return paper


def find_shape(cell):
    """Is shape and X or an O?"""
    mapper = {0: None, 1: 'X', 2: 'O'}
    cell = detections.preprocess_input(cell)
    idx = np.argmax(model.predict(cell))
    return mapper[idx]


def get_board_template(thresh):
    """Returns 3 x 3 grid, a.k.a the board"""
    # Find grid's center cell, and based on it fetch
    # the other eight cells
    middle_center = detections.contoured_bbox(thresh)
    center_x, center_y, width, height = middle_center

    # Useful coords
    left = center_x - width
    right = center_x + width
    top = center_y - height
    bottom = center_y + height

    # Middle row
    middle_left = (left, center_y, width, height)
    middle_right = (right, center_y, width, height)
    # Top row
    top_left = (left, top, width, height)
    top_center = (center_x, top, width, height)
    top_right = (right, top, width, height)
    # Bottom row
    bottom_left = (left, bottom, width, height)
    bottom_center = (center_x, bottom, width, height)
    bottom_right = (right, bottom, width, height)

    # Grid's coordinates
    return [top_left, top_center, top_right,
            middle_left, middle_center, middle_right,
            bottom_left, bottom_center, bottom_right]


def draw_shape(template, shape, coords):
    """Draw on a cell the shape which resides in it"""
    x, y, w, h = coords
    if shape == 'O':
        centroid = (x + int(w / 2), y + int(h / 2))
        cv2.circle(template, centroid, 10, (0, 0, 0), 2)
    elif shape == 'X':
        # Draws the 'X' shape
        cv2.line(template, (x + 10, y + 7), (x + w - 10, y + h - 7),
                 (0, 0, 0), 2)
        cv2.line(template, (x + 10, y + h - 7), (x + w - 10, y + 7),
                 (0, 0, 0), 2)
    return template


def player(image_path):
    """Play tic tac toe game with computer that uses the alphabeta algorithm"""
    # Initialize opponent (computer)
    history = {}
    board_info = []
    # Read the image

    frame = cv2.imread(image_path)

    # Preprocess input
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)

    thresh = cv2.GaussianBlur(thresh, (7, 7), 0)

    paper = find_sheet_paper(frame)

    # Four red dots must appear on each corner of the sheet of paper,
    # otherwise try moving it until they're well detected

    # Now working with 'paper' to find grid
    paper_gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)

    _, paper_thresh = cv2.threshold(
        paper_gray, 170, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("python_images/thresh_paper.jpg",  paper_thresh)
    grid = get_board_template(paper_thresh)

    for i, (x, y, w, h) in enumerate(grid):
        griddy_paper = cv2.rectangle(paper, (x, y), (x + w, y + h), (0, 0, 0), 2)
        cv2.imwrite("python_images/griddy_paper.jpg",griddy_paper)

    for i, (x, y, w, h) in enumerate(grid):
        # Find what is inside each free cell
        cell = paper_thresh[int(y): int(y + h), int(x): int(x + w)]
        shape = find_shape(cell)
        board_info.append(shape)

    print(board_info)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(args):
    """Check if everything's okay and start game"""
    # Load model
    global model
    assert os.path.exists(args.model), '{} does not exist'
    model = load_model(args.model)
    # Announce winner!
    player(args.image_path)
    sys.exit()
if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
