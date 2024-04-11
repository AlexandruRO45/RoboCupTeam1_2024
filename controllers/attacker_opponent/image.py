import threading
import queue
from collections import namedtuple
import cv2
import numpy as np

class FrameBuffer:
    """ Class to represent a buffer for storing and accessing image frames. """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = queue.Queue(maxsize=3)

    def put_frame(self, frame):
        """ Pushes an image frame to the buffer if space is available. """
        if frame.shape[:2] != (self.height, self.width):
            raise ValueError(f"Invalid frame size. Expected: {(self.height, self.width)}, Got: {frame.shape[:2]}")
        self.buffer.put(frame)

    def get_frame(self, timeout=0.1):
        """ Retrieves an image frame from the buffer if available within the timeout. Raises an exception if no frame is available. """
        try:
            return self.buffer.get(timeout=timeout)
        except queue.Empty:
            raise TimeoutError("No frame available in the buffer")

class ImageStreamer(threading.Thread):
    """ Thread-based class for capturing images from a camera and storing them in a frame buffer. """
    def __init__(self, capture_device, frame_buffer):
        super().__init__(daemon=True)
        self.capture_device = capture_device
        self.frame_buffer = frame_buffer
        self.running = True
        self.prev_ball_x = None  # Store previous ball x-coordinate

    def run(self):
        while self.running:
            ret, frame = self.capture_device.read()
            if ret:
                # Ball detection logic (e.g., color-based segmentation)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                lower_color = np.array([29, 86, 6])
                upper_color = np.array([64, 255, 255])
                mask = cv2.inRange(hsv, lower_color, upper_color)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if contours:
                    # Find the largest contour (assuming it's the ball)
                    largest_contour = max(contours, key=cv2.contourArea)

                    # Calculate ball center
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        ball_x = int(M["m10"] / M["m00"])
                        ball_y = int(M["m01"] / M["m00"])

                        # Draw vertical line at center
                        height, width, _ = frame.shape
                        cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 0), 2)

                        # Determine ball direction
                        if self.prev_ball_x is not None:
                            if ball_x < self.prev_ball_x:
                                print("Left")
                            else:
                                print("Right")

                        self.prev_ball_x = ball_x  # Update previous ball x-coordinate

                self.frame_buffer.put_frame(frame)
            else:
                print("Failed to capture image frame.")

    def stop(self):
        self.running = False

# Example usage
capture_device = cv2.VideoCapture(0)  # Assuming camera index 0
frame_buffer = FrameBuffer(width=640, height=480)
streamer = ImageStreamer(capture_device, frame_buffer)
streamer.start()

# Simulate processing frames from the buffer in a loop
while True:
    try:
        frame = frame_buffer.get_frame()
        cv2.imshow("Image Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except TimeoutError:
        print("No frame available to process.")

streamer.stop()
capture_device.release()
cv2.destroyAllWindows()