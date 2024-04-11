"""Game of tic tac toe using OpenCV to play against computer"""

import os
import sys
import cv2
import argparse
import numpy as np
import time
from keras.models import load_model
from data.utils import auto_corner_detection
from data.utils import detections
import requests
import json


SERVER_URL_ARRAY_POST= "http://martin-upward-lately.ngrok-free.app/array" 
SERVER_URL_ARRAY_READY_FLAG = "http://martin-upward-lately.ngrok-free.app/array/state"

headers = {
    'Content-Type': 'application/json'
}

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--image_path", help="path to image file")

    parser.add_argument('--model', '-m', type=str, default='data/model.h5',
                        help='model file (.h5) to detect Xs and Os')

    return parser.parse_args()


# def find_sheet_paper(frame, thresh, add_margin=True):
def find_sheet_paper(frame):
    """Detect the coords of the sheet of paper the game will be played on"""
    paper = auto_corner_detection.auto_corner(frame)
    return paper


def find_shape(cell):
    """Is shape and X or an O?"""
    mapper = {0: " ", 1: 'X', 2: 'O'}
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


def populate(image_path):
    """Populate the board with the shapes found in the cells of the grid"""
    board_info = []
    # Read the image

    frame = cv2.imread(image_path)

    # Preprocess input
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)

    thresh = cv2.GaussianBlur(thresh, (7, 7), 0)

    paper = find_sheet_paper(frame)
    # Now working with 'paper' to find grid
    paper_gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)

    _, paper_thresh = cv2.threshold(
        paper_gray, 170, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("opencv_images/thresh_paper.jpg",  paper_thresh)
    grid = get_board_template(paper_thresh)

    for i, (x, y, w, h) in enumerate(grid):
        griddy_paper = cv2.rectangle(paper, (x, y), (x + w, y + h), (0, 0, 0), 2)
        cv2.imwrite("opencv_images/griddy_paper.jpg",griddy_paper)

    for i, (x, y, w, h) in enumerate(grid):
        # Find what is inside each free cell
        cell = paper_thresh[int(y): int(y + h), int(x): int(x + w)]
        shape = find_shape(cell)
        board_info.append(shape)

    print(board_info)
    print(type(board_info))
    return board_info
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function to continuously monitor a directory for new images
def monitor_directory(directory):
    while True:
        for filename in os.listdir(directory):
            if filename.endswith(".jpg"):  # Adjust the file extension as needed
                image_path = os.path.join(directory, filename)
                process_and_send_image(image_path)  # Process the image and send to the server
                os.remove(image_path)  # Optionally, remove the processed image after sending
        time.sleep(1)  # Adjust the sleep time as needed
import time

def send_with_retry(url, payload, headers, max_retries=3, retry_delay=3):
    """
    Attempt to send a POST request up to max_retries times.

    :param url: The URL to send the POST request to.
    :param payload: The JSON payload to be sent.
    :param headers: Headers for the request.
    :param max_retries: Maximum number of retry attempts.
    :param retry_delay: Delay between retries in seconds.
    :return: The response object if successful, None if not.
    """
    for attempt in range(max_retries):
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Request successful.")
            return response
        else:
            print(f"Attempt {attempt + 1} failed with status code {response.status_code}. Retrying...")
            time.sleep(retry_delay)
    print("Max retries reached. Request failed.")
    return None  # Indicates failure after all attempts


def process_and_send_image(image_path):
    try:
        # Perform image processing to get the new game state
        new_array = populate(image_path)
        
        # Prepare the payload
        payload1 =  new_array
        payload2 = {"is_ready":True}

        # Use the send_with_retry function to attempt sending the data
        response1 = send_with_retry(SERVER_URL_ARRAY_READY_FLAG, payload2, headers)
        response2 = send_with_retry(SERVER_URL_ARRAY_POST, payload1, headers)
        # Optionally, check the response here if additional handling is needed
        if response1 and response2:
           print("Data sent successfully.")
        else:
            print("Error sending data to server.")
    except Exception as e:
        print(f"Error processing image: {e}")


# def main(args):
#     """Check if everything's okay and start game"""
#     # Load model
#     global model
#     assert os.path.exists(args.model), '{} does not exist'
#     model = load_model(args.model)
#     populate(args.image_path)
#     sys.exit()
# if __name__ == '__main__':
#     main(parse_arguments(sys.argv[1:]))


def main():
    # Directory to monitor for new images
    # Load model
    global model
    model = load_model("data/model.h5")
    image_directory = r"C:\Users\eltac\Desktop\VS_CODE\tic-tac-toe\tic-tac-toe\active_images_repo"
    monitor_directory(image_directory)
    
if __name__ == "__main__":
    main()