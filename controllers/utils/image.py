import threading
import queue
from collections import namedtuple

import cv2
import numpy as np


class FrameBuffer:
    """
    Class to represent a buffer for storing and accessing image frames.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = queue.Queue(maxsize=3)

    def put_frame(self, frame):
        """
        Pushes an image frame to the buffer if space is available.
        """
        if frame.shape[:2] != (self.height, self.width):
            raise ValueError(f"Invalid frame size. Expected: {(self.height, self.width)}, Got: {frame.shape[:2]}")
        self.buffer.put(frame)

    def get_frame(self, timeout=0.1):
        """
        Retrieves an image frame from the buffer if available within the timeout.
        Raises an exception if no frame is available.
        """
        try:
            return self.buffer.get(timeout=timeout)
        except queue.Empty:
            raise TimeoutError("No frame available in the buffer")


class ImageStreamer(threading.Thread):
    """
    Thread-based class for capturing images from a camera and storing them in a frame buffer.
    """

    def __init__(self, capture_device, frame_buffer):
        super().__init__(daemon=True)
        self.capture_device = capture_device
        self.frame_buffer = frame_buffer
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.capture_device.read()
            if ret:
                self.frame_buffer.put_frame(frame)
            else:
                print("Failed to capture image frame.")

    def stop(self):
        self.running = False


# # Example usage
# # Modify capture device and frame buffer parameters as needed
# capture_device = cv2.VideoCapture(0)  # Assuming camera index 0
# frame_buffer = FrameBuffer(width=640, height=480)

# streamer = ImageStreamer(capture_device, frame_buffer)
# streamer.start()

# # Simulate processing frames from the buffer in a loop
# for _ in range(5):
#     try:
#         frame = frame_buffer.get_frame()
#         # Process frame (e.g., using OpenCV)
#         cv2.imshow("Image Stream", frame)
#         cv2.waitKey(1)
#     except TimeoutError:
#         print("No frame available to process.")

# streamer.stop()
# capture_device.release()
# cv2.destroyAllWindows()
