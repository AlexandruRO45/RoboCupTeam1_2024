import cv2
import numpy as np
from controller import Robot, Camera, Motion

class Nao(Robot):
    def __init__(self):
        Robot.__init__(self)
        self.timeStep = int(self.getBasicTimeStep())
        self.currentlyPlaying = False
        self.loadMotionFiles()
        self.findAndEnableDevices()
        self.lowerHands()

    def loadMotionFiles(self):
        self.forwards = Motion('../../motions/Forwards50.motion')
        self.HandWave = Motion('../../motions/HandWave.motion')

    def startMotion(self, motion):
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()
        motion.play()
        self.currentlyPlaying = motion

    def lowerHands(self):
        # Set angles to lower the hands
        for i in range(0, 6):
            self.RShoulderPitch.setPosition(2)  # Adjust angles as needed
            self.LShoulderPitch.setPosition(2)  # Adjust angles as needed

    def findAndEnableDevices(self):
        # Upper camera
        self.upperCamera = self.getDevice("CameraTop")
        self.upperCamera.enable(self.timeStep)

        # Lower camera
        self.lowerCamera = self.getDevice("CameraBottom")
        self.lowerCamera.enable(self.timeStep)

        # shoulder pitch motors
        self.RShoulderPitch = self.getDevice("RShoulderPitch")
        self.LShoulderPitch = self.getDevice("LShoulderPitch")

        # ultrasonic sensors (for backup)
        self.us = []
        usNames = ['Sonar/Left', 'Sonar/Right']
        for name in usNames:
            self.us.append(self.getDevice(name))
            if self.us[-1] is not None:
                self.us[-1].enable(self.timeStep)
    
    def ballDetected(self, camera, max_distance):
        # Get the camera image
        image = camera.getImage()
        if image is not None:
            # Convert the image to a numpy array
            image_array = np.frombuffer(image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))

            # Convert the image to BGR format
            frame = cv2.cvtColor(image_array, cv2.COLOR_BGRA2BGR)

            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define range of orange color in HSV
            lower_orange = np.array([0, 150, 50])
            upper_orange = np.array([50, 255, 255])

            # Threshold the HSV image to get only orange colors
            mask = cv2.inRange(hsv, lower_orange, upper_orange)

            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame, frame, mask=mask)

            # Convert to grayscale
            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Use Canny edge detector
            edges = cv2.Canny(blurred, 50, 150)

            # Use Hough Circle Transform to find circles
            circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=2, minDist=120,
                                        param1=120, param2=50, minRadius=1, maxRadius=300)

            # If circles are detected within the maximum distance, return True
            if circles is not None:
                for circle in circles[0, :]:
                    x, y, _ = circle
                    distance = self.calculateDistance(x, y, camera)
                    if distance < max_distance:
                        return True
        return False
    
    def calculateDistance(self, x, y, camera):
        # Calculate the distance between the detected object and the camera
        fov = camera.getFov()
        width = camera.getWidth()
        angle = fov * (x / width - 0.5)
        distance = (camera.getHeight() / 2) / np.tan(angle)
        return distance

    def run(self):
        while self.step(self.timeStep) != -1:
            # Check if a ball is detected within a certain distance in either camera
            if self.ballDetected(self.upperCamera, max_distance=500) or self.ballDetected(self.lowerCamera, max_distance = 500 ):
                # Stop walking
                print('ball detected')
                self.forwards.stop()

                # Perform SideStepLeft motion three times
                for _ in range(3):  # Changed to 3 times as mentioned in your comment
                    self.startMotion(self.HandWave)

                    # Wait for the motion to complete (adjust time as needed)
                    self.step(5000)

                    # Start walking forwards again
                    self.startMotion(self.forwards)

                    # Wait for a while before checking sensors again
                    self.step(1)  # Adjust this delay as needed
            else:
                # Start walking forwards if no ball is detected
                self.startMotion(self.forwards)


# Create the Robot instance and run main loop
robot = Nao()
robot.run()
