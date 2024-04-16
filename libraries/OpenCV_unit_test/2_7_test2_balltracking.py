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
        # Additional motions
        self.sidestepright = Motion('../../motions/SideStepRight.motion')
        self.sidestepleft = Motion('../../motions/SideStepLeft.motion')
        self.turnleft40 = Motion('../../motions/TurnLeft40.motion')
        self.turnleft60 = Motion('../../motions/TurnLeft60.motion')
        self.turnleft180 = Motion('../../motions/TurnLeft180.motion')
        self.turnright40 = Motion('../../motions/TurnRight40.motion')
        self.turnright60 = Motion('../../motions/TurnRight60.motion')

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
            if self.ballDetected(self.upperCamera, max_distance=500) or self.ballDetected(self.lowerCamera, max_distance=500):
                # Stop walking
                print('ball detected')
                self.forwards.stop()

                # Determine the position of the ball
                ball_position = self.getBallPosition()

                # Perform the appropriate sidestep motion based on ball position
                if ball_position == "left":
                    self.startMotion(self.sidestepleft)
                elif ball_position == "right":
                    self.startMotion(self.sidestepright)

                # Wait for the motion to complete
                self.step(3000)  # Adjust time as needed

                # Start walking forwards again
                self.startMotion(self.forwards)
            else:
                # Start walking forwards if no ball is detected
                self.startMotion(self.forwards)

    def getBallPosition(self):
        # Get the camera image
        image = self.upperCamera.getImage()
        if image is not None:
            # Convert the image to a numpy array
            image_array = np.frombuffer(image, np.uint8).reshape((self.upperCamera.getHeight(), self.upperCamera.getWidth(), 4))

            # Convert the image to BGR format
            frame = cv2.cvtColor(image_array, cv2.COLOR_BGRA2BGR)

            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define range of orange color in HSV
            lower_orange = np.array([0, 150, 50])
            upper_orange = np.array([50, 255, 255])

            # Threshold the HSV image to get only orange colors (ball)
            mask = cv2.inRange(hsv, lower_orange, upper_orange)

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Initialize variables to track ball position
            ball_position = None

            # If contours are found
            if contours:
                # Find the largest contour (presumably the ball)
                largest_contour = max(contours, key=cv2.contourArea)

                # Get the bounding rectangle of the contour
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Determine the position of the ball based on its centroid
                centroid_x = x + w // 2
                centroid_y = y + h // 2
                image_center_x = self.upperCamera.getWidth() // 2

                if centroid_x < image_center_x:
                    ball_position = "left"
                else:
                    ball_position = "right"

            return ball_position

        else:
            # If no image is received, return None
            return None

# Create the Robot instance and run main loop
robot = Nao()
robot.run()
