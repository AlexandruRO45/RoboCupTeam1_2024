import cv2
import numpy as np
import torch
from controller import Robot, Camera, Motion

# Load the YOLOv5s model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='../../plugins/yolov5/yolov5s.pt', trust_repo=True)

class Nao(Robot):
    def __init__(self):
        Robot.__init__(self)
        self.timeStep = int(self.getBasicTimeStep())
        self.currentlyPlaying = False
        self.loadMotionFiles()
        self.findAndEnableDevices()
        self.lowerHands()    
        # Define object detection function with OpenCV integration
        def detect_objects(frame):
            # Resize frame to match YOLO model's expected input size, e.g., 416x416
            resized_frame = cv2.resize(frame, (416, 416))

            # Convert frame to RGB format and normalize
            tensor = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            tensor = np.transpose(tensor, (2, 0, 1))  # Change from HWC to CHW format
            tensor = torch.from_numpy(tensor).float().unsqueeze(0) / 255.0  # Add batch dimension and normalize

            # Perform inference
            results = model(tensor)

            # Debugging: Print the type and attributes of the results object
            print(f"Results object type: {type(results)}")
            # If it's a custom object, this will help identify available methods/attributes
            if not isinstance(results, (list, tuple, torch.Tensor)):
                print(f"Results attributes/methods: {dir(results)}")

            # Temporarily return an empty list to avoid errors while inspecting
            return []
        
        self.detect_objects = detect_objects

    def loadMotionFiles(self):
        self.forwards = Motion('../../plugins/motions/Forwards50.motion')
        self.turnLeft = Motion('../../plugins/motions/TurnLeft60.motion')
        self.turnRight = Motion('../../plugins/motions/TurnRight60.motion')

    def startMotion(self, motion):
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()
        motion.play()
        self.currentlyPlaying = motion

    def lowerHands(self):
        # Set angles to lower the hands
        for i in range(0, 6):
            self.RShoulderPitch.setPosition(0.9)  # Adjust angles as needed
            self.LShoulderPitch.setPosition(0.9)  # Adjust angles as needed

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
            # Convert to NumPy array
            image_array = np.frombuffer(image, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))

            # Perform object detection using YOLOv5s
            boxes = self.detect_objects(image_array)

            # Check for detected balls within the maximum distance
            for box in boxes:
                x1, y1, x2, y2 = box
                width = x2 - x1
                height = y2 - y1
                center_x = x1 + width / 2
                center_y = y1 + height / 2
                distance = self.calculateDistance(center_x, center_y, camera)
                if distance < max_distance and box[5] == 0:  # Assuming class 0 represents balls
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
            # Check if a ball is detected within a certain distance
            if self.ballDetected(self.upperCamera, max_distance=2.0) or self.ballDetected(self.lowerCamera, max_distance=2.0):
                # Stop walking
                self.forwards.stop()

                # Turn 180 degrees based on which side has more space (backup using ultrasonic sensors)
                if self.us[0].getValue() > self.us[1].getValue():
                    self.startMotion(self.turnRight)
                else:
                    self.startMotion(self.turnLeft)

                # Wait for the turn to complete (approx. 3 seconds)
                self.step(3000)

                # Start walking forwards again
                self.startMotion(self.forwards)

                # Wait for a while before checking sensors again
                self.step(5000)  # Adjust this delay as needed
            else:
                # Start walking forwards if no ball is detected
                self.startMotion(self.forwards)


# Create the Robot instance and run main loop
robot = Nao()
robot.run()