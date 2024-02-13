import cv2


# Open the webcam
def image_capture():
    cap = cv2.VideoCapture(0)  # 0 indicates the default camera, you can change it if you have multiple cameras

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
    else:
        # Capture a single frame
        ret, frame = cap.read()

        # Check if the frame is captured successfully
        if ret:
            # Save the captured frame to an image file
            cv2.imwrite('python_images/captured_image.jpg', frame)
            print("Image captured successfully.")
        else:
            print("Error: Could not capture frame.")

        # Release the camera
        cap.release()
        # Close all OpenCV windows
        cv2.destroyAllWindows()
        return frame
