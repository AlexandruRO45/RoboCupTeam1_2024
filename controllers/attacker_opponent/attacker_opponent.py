from controller import Robot, Motion
from collections import defaultdict
import time
import cv2
import numpy as np
import math

class NaoSoccerBallDetector:
    def __init__(self, robot):
        self.robot = robot
        self.prev_ball_x = None  # Store previous ball x-coordinate
        self.track_history = defaultdict(lambda: []) # Store the track history
        self.track = [] # Store the track
        self.time_step = int(robot.getBasicTimeStep())
        self.camera_bottom = robot.getDevice("CameraBottom")
        self.camera_bottom.enable(self.time_step)
        self.camera_top = robot.getDevice("CameraTop")
        self.camera_top.enable(self.time_step)
        self.width_bottom = self.camera_bottom.getWidth()
        self.height_bottom = self.camera_bottom.getHeight()
        self.width_top = self.camera_top.getWidth()
        self.height_top = self.camera_top.getHeight()
        self.accelerometer = robot.getDevice("accelerometer")
        self.accelerometer.enable(4 * self.time_step)

    def detect_soccer_ball(self):
        # Get the image from the bottom camera
        image_bottom = self.camera_bottom.getImage()
        if not image_bottom:
            return None

        # Convert image to numpy array
        image_bottom = np.frombuffer(image_bottom, np.uint8).reshape((self.height_bottom, self.width_bottom, 4))

        # Convert image from RGBA to RGB
        image_bottom = cv2.cvtColor(image_bottom, cv2.COLOR_RGBA2RGB)

        # Define lower and upper bounds for the soccer ball color (black and white)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([70, 70, 70])
        lower_white = np.array([200, 200, 200])
        upper_white = np.array([255, 255, 255])

        # Threshold the image to get only black and white colors
        mask_black = cv2.inRange(image_bottom, lower_black, upper_black)
        mask_white = cv2.inRange(image_bottom, lower_white, upper_white)

        # Find contours of the black areas (soccer ball) and white areas (goal post)
        contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_white, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are found for both black and white areas
        if contours_black and contours_white:
            largest_contour_black = max(contours_black, key=cv2.contourArea)
            largest_contour_white = max(contours_white, key=cv2.contourArea)

            moments_black = cv2.moments(largest_contour_black)
            moments_white = cv2.moments(largest_contour_white)

            if moments_black["m00"] != 0 and moments_white["m00"] != 0:
                ball_position_x = int(moments_black["m10"] / moments_black["m00"])
                ball_position_y = int(moments_black["m01"] / moments_black["m00"])

                # Look down if the ball is near the robot's feet
                if ball_position_y > 0.8 * self.height_bottom:
                    self.look_down()

                goal_post_position_x = int(moments_white["m10"] / moments_white["m00"])
                goal_post_position_y = int(moments_white["m01"] / moments_white["m00"])

                # Implement ball trajectory tracking
                if self.prev_ball_x is not None:
                    if ball_position_x < self.prev_ball_x:
                        print("Left")
                    else:
                        print("Right")

                self.prev_ball_x = ball_position_x  # Update previous ball x-coordinate

                return ball_position_x, ball_position_y, goal_post_position_x, goal_post_position_y

        return None

    def detect_other_robot(self):
        # Get the image from the top camera
        image_top = self.camera_top.getImage()
        if not image_top:
            return False

        # Convert image to numpy array
        image_top = np.frombuffer(image_top, np.uint8).reshape((self.height_top, self.width_top, 4))
        
        # Convert image from RGBA to RGB
        image_top = cv2.cvtColor(image_top, cv2.COLOR_RGBA2RGB)

        # Define lower and upper bounds for detecting other robots
        lower_robot = np.array([0, 0, 0])
        upper_robot = np.array([255, 255, 255])

        # Threshold the image to get only robot colors
        mask_robot = cv2.inRange(image_top, lower_robot, upper_robot)

        # Find contours of the robot areas
        contours_robot, _ = cv2.findContours(mask_robot, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are found for robots
        if contours_robot:
            for contour in contours_robot:
                area = cv2.contourArea(contour)
                if area > 100:  # Minimum area threshold to consider as a robot
                    return True
        return False

    def look_down(self):
        self.robot.getDevice("HeadPitch").setPosition(0.5)  # Adjust the value to control the head pitch

    def detect_goal_post(self):
        # Get the image from the bottom camera
        image_bottom = self.camera_bottom.getImage()
        if not image_bottom:
            return None

        # Convert image to numpy array
        image_bottom = np.frombuffer(image_bottom, np.uint8).reshape((self.height_bottom, self.width_bottom, 4))
        
        # Convert image from RGBA to RGB
        image_bottom = cv2.cvtColor(image_bottom, cv2.COLOR_RGBA2RGB)

        # Define lower and upper bounds for detecting the black goal post
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([70, 70, 70])

        # Threshold the image to get only black color (goal post)
        mask_black = cv2.inRange(image_bottom, lower_black, upper_black)

        # Find contours of the black areas (goal post)
        contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are found for black areas (goal post)
        if contours_black:
            largest_contour_black = max(contours_black, key=cv2.contourArea)
            moments_black = cv2.moments(largest_contour_black)
            if moments_black["m00"] != 0:
                goal_post_position_x = int(moments_black["m10"] / moments_black["m00"])
                goal_post_position_y = int(moments_black["m01"] / moments_black["m00"])
                return goal_post_position_x, goal_post_position_y
        return None

class NaoRobot:
    def __init__(self):
        self.robot = Robot()
        self.detector = NaoSoccerBallDetector(self.robot)
        self.time_step = int(self.robot.getBasicTimeStep())

        # Initialize accelerometer
        self.accelerometer = self.robot.getDevice("accelerometer")
        self.accelerometer.enable(4 * self.time_step)

        # Initialize motion and forward motion file
        self.motion = self.robot.getDevice('WEBOTS_MOTION')
        self.forwards = Motion('../../plugins/motions/Forwards50.motion')

        # Initialize left and right motors
        self.left_motor = self.robot.getDevice('LAnklePitch')
        self.right_motor = self.robot.getDevice('RAnklePitch')
        self.RShoulderPitch = self.robot.getDevice("RShoulderPitch")
        self.LShoulderPitch = self.robot.getDevice("LShoulderPitch")

        # Check if motor devices were successfully initialized
        if self.left_motor is None or self.right_motor is None:
            print("Error: Failed to initialize motor devices.")
        else:
            # Set position and velocity for motors
            self.left_motor.setPosition(float('inf'))
            self.right_motor.setPosition(float('inf'))
            self.left_motor.setVelocity(0.0)
            self.right_motor.setVelocity(0.0)

        self.kp_linear = 0.1  # Proportional control gain for linear velocity
        self.kp_angular = 0.1  # Proportional control gain for angular velocity

        self.target_position = (3.23016, -0.0560672, 0.0696783)  # Target position
        self.stop_radius = 0.25  # Stop radius in meters

    def calculate_linear_velocity(self, distance):
        return self.kp_linear * distance

    def calculate_angular_velocity(self, angle):
        return self.kp_angular * angle

    def navigate_to_goal_post(self, ball_position, goal_position):
        ball_x, ball_y = ball_position
        goal_x, goal_y, goal_z = goal_position

        # Calculate the distance between the ball and the goal post
        distance = math.sqrt((goal_x - ball_x) ** 2 + (goal_y - ball_y) ** 2)

        # Calculate the angle between the current orientation and the direction towards the goal post
        angle = math.atan2(goal_y - ball_y, goal_x - ball_x)

        # Calculate linear and angular velocities based on distance and angle
        linear_velocity = self.calculate_linear_velocity(distance)
        angular_velocity = self.calculate_angular_velocity(angle)

        # Set the velocities to move the robot
        left_velocity = linear_velocity - angular_velocity
        right_velocity = linear_velocity + angular_velocity
        self.left_motor.setVelocity(left_velocity)
        self.right_motor.setVelocity(right_velocity)

    def navigate_to_other_robot(self, ball_position, other_robot_position):
        ball_x, ball_y = ball_position
        other_robot_x, other_robot_y, other_robot_z = other_robot_position

        # Calculate the distance between the ball and the other robot
        distance = math.sqrt((other_robot_x - ball_x) ** 2 + (other_robot_y - ball_y) ** 2)

        # Calculate the angle between the current orientation and the direction towards the other robot
        angle = math.atan2(other_robot_y - ball_y, other_robot_x - ball_x)

        # Calculate linear and angular velocities based on distance and angle
        linear_velocity = self.calculate_linear_velocity(distance)
        angular_velocity = self.calculate_angular_velocity(angle)

        # Set the velocities to move the robot
        left_velocity = linear_velocity - angular_velocity
        right_velocity = linear_velocity + angular_velocity
        self.left_motor.setVelocity(left_velocity)
        self.right_motor.setVelocity(right_velocity)

    def walk_forward(self):
        self.forwards.play()

    def stop_walk(self):
        self.forwards.stop()

    def kick_ball(self):
        # Load kicking motion file
        self.kick_motion = Motion('../../plugins/motions/Shoot.motion')
        self.kick_motion.play()

    # def stand_up_(self):
    #     # Load stand-up motion file
    #     stand_up_front_motion = Motion('../../plugins/motions/StandUpFromFront.motion')
    #     stand_up_back_motion = Motion('../../plugins/motions/StandUpFromBack.motion')
    #     if self.detect_fall() == self.stand_up_front:
    #         stand_up_front_motion.play()
    #     elif self.detect_fall() == self.stand_up_back:
    #         stand_up_back_motion.play()

    def stand_up_(self):
        """
        Attempts to stand up the robot based on the fall direction.

        This function assumes the robot can detect its fall using an accelerometer 
        (implementation not provided) and assigns fall direction based on 
        accelerometer readings (provided in the original code).

        Needs appropriate motion files (e.g., StandUpFromFront.motion) loaded 
        before playing them. 
        """

        stand_up_motion = None  # Initialize stand_up_motion variable

        # Determine fall direction based on accelerometer readings (provided in original code)
        fall_direction = self.detect_fall()

        # Select appropriate stand-up motion based on fall direction
        if fall_direction == self.stand_up_front:
            stand_up_motion = Motion('../../plugins/motions/StandUpFromFront.motion')
        elif fall_direction == self.stand_up_back:
            stand_up_motion = Motion('../../plugins/motions/StandUpFromBack.motion')

        # Play the stand-up motion if a valid direction is detected
        if stand_up_motion:
            stand_up_motion.play()

    def detect_fall(self):
        """
        Detects falls based on accelerometer readings.

        This is a basic implementation that checks for significant acceleration 
        in a specific direction (e.g., forward or backward tilt) to indicate 
        a potential fall.

        In practice, fall detection can be more complex and might require 
        additional sensors or algorithms.
        """

        # Get accelerometer values
        acc = self.accelerometer.getValues(self.time_step)  # Include time_step argument

        # Thresholds for fall detection (adjust based on robot calibration)
        fall_threshold = 5.0  # Acceleration threshold
        forward_fall_limit = -0.7  # Minimum Z-axis value for forward fall
        backward_fall_limit = 0.7  # Maximum Z-axis value for backward fall

        # Detect forward fall
        if (
            math.fabs(acc[0]) > math.fabs(acc[1])
            and math.fabs(acc[0]) > math.fabs(acc[2])
            and acc[0] < -fall_threshold
            and acc[2] < forward_fall_limit
        ):
            return self.stand_up_front  # Indicate front fall

        # Detect backward fall
        elif (
            math.fabs(acc[0]) > math.fabs(acc[1])
            and math.fabs(acc[0]) > math.fabs(acc[2])
            and acc[0] > fall_threshold
            and acc[2] > backward_fall_limit
        ):
            return self.stand_up_back  # Indicate back fall

        # No fall detected
        else:
            return None

    # def detect_fall(self):
    #     # Get accelerometer values
    #     acc = self.accelerometer.getValues()
    #     if (
    #         math.fabs(acc[0]) > math.fabs(acc[1])
    #         and math.fabs(acc[0]) > math.fabs(acc[2])
    #         and acc[0] < -5
    #     ):
    #         return self.stand_up_front
    #     elif (
    #         math.fabs(acc[0]) > math.fabs(acc[1])
    #         and math.fabs(acc[0]) > math.fabs(acc[2])
    #         and acc[2] > 0
    #     ):
    #         return self.stand_up_back
        
    def stabilize(self):
        # Set angles to lower the hands
        for i in range(0, 10):
            self.RShoulderPitch.setPosition(2)  # Adjust angles as needed
            self.LShoulderPitch.setPosition(2)  # Adjust angles as needed

    def run(self):
        while self.robot.step(self.time_step) != -1:
            ball_position = self.detector.detect_soccer_ball()
            goal_position = (5, 5, 5)  # Assuming the goal post's position is fixed
            
            if ball_position:
                ball_position_x, ball_position_y, goal_post_position_x, goal_post_position_y = ball_position
                print("Attacker Detected Soccer Ball Position:", (ball_position_x, ball_position_y))
                print("Detected Goal Post Position:", (goal_post_position_x, goal_post_position_y))
                
                # Calculate the distance and direction to the goal post
                goal_distance = math.sqrt((goal_post_position_x - ball_position_x) ** 2 + (goal_post_position_y - ball_position_y) ** 2)
                goal_direction = math.atan2(goal_post_position_y - ball_position_y, goal_post_position_x - ball_position_x)

                print("Distance to Goal Post:", goal_distance)
                print("Direction to Goal Post:", goal_direction)
                
                # Perform stabilization before initiating any movement
                self.stabilize()
                
                # Navigate to the goal post
                self.navigate_to_goal_post((ball_position_x, ball_position_y), goal_position)
                
                # Start walking forward
                self.walk_forward()
                
                # Check if the goal post is near enough to kick the ball
                if abs(ball_position_x - goal_post_position_x) < 10:  # Adjust the threshold as needed
                    # Look straight
                    self.robot.getDevice("HeadPitch").setPosition(0.0)  # Adjust the value to look straight
                    # Kick the ball
                    self.kick_ball()
            else:
                print("Soccer ball not detected.")
                self.stop_walk()  # Stop walking if ball is not detected
                
            # Detect other robots and navigate towards them
            if self.detector.detect_other_robot():
                print("Another robot detected. Navigating towards it.")
                other_robot_position = (5, 5, 5)  # Assuming the other robot's position
                #self.navigate_to_other_robot((ball_position_x, ball_position_y), other_robot_position)

               
            # Detect black goal post
            goal_post_position = self.detector.detect_goal_post()
            if goal_post_position:
                print("Black Goal Post Detected:", goal_post_position)

if __name__ == "__main__":
    nao_robot = NaoRobot()
    nao_robot.run()
