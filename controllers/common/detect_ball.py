import cv2
import numpy as np
from controller import Camera

def detect_ball(camera: Camera):
    """
    Detects a black and white soccer ball using the robot's camera.

    Args:
        camera (Camera): The camera object to capture images.

    Returns:
        tuple: (detected, x, y) where 'detected' is a boolean indicating if the ball is detected,
               and 'x', 'y' are the normalized coordinates of the ball in the image frame.
    """
    width, height = camera.getWidth(), camera.getHeight()
    image = camera.getImageArray()
    
    # Convert image to a format suitable for OpenCV processing
    image_cv = np.frombuffer(camera.getImage(), np.uint8).reshape((height, width, 4))
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGRA2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve detection accuracy
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image to isolate the ball. Adjust the threshold values as needed.
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected = False
    ball_x, ball_y = -1, -1  # Initialize ball position to an invalid state

    # Loop over the contours
    for contour in contours:
        # Approximate the contour
        ((x, y), radius) = cv2.minEnclosingCircle(contour)

        # Filter out small contours that are likely not the ball
        if radius > 5:  # Radius threshold, adjust based on your simulation scale
            detected = True
            ball_x, ball_y = (x / width, y / height)  # Normalize coordinates to [0, 1]
            break  # Assuming only one ball, break after the first detected ball

    return detected, ball_x, ball_y
