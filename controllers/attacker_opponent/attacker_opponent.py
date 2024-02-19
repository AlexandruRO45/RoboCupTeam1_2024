from controller import Robot, Motion
import cv2
import numpy as np
import math

class NaoSoccerBallDetector:
    def __init__(self, robot):
        self.robot = robot
        self.time_step = int(robot.getBasicTimeStep())
        self.camera = robot.getDevice("CameraBottom")
        self.camera.enable(self.time_step)
        self.width = self.camera.getWidth()
        self.height = self.camera.getHeight()

    def detect_soccer_ball(self):
        # Get the image from the camera
        image = self.camera.getImage()
        if not image:
            return None

        # Convert image to numpy array
        image = np.frombuffer(image, np.uint8).reshape((self.height, self.width, 4))
        
        # Convert image from RGBA to RGB
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        # Define lower and upper bounds for the soccer ball color (black and white)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([70, 70, 70])

        # Threshold the image to get only black colors
        mask = cv2.inRange(image, lower_black, upper_black)

        # Find contours of the black areas
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are found, calculate the center of the largest contour
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            moments = cv2.moments(largest_contour)
            if moments["m00"] != 0:
                ball_position_x = int(moments["m10"] / moments["m00"])
                ball_position_y = int(moments["m01"] / moments["m00"])
                
                # Look down if the ball is near the robot's feet
                if ball_position_y > 0.8 * self.height:
                    self.look_down()
                
                return ball_position_x, ball_position_y
        return None

    def look_down(self):
        self.robot.getDevice("HeadPitch").setPosition(0.5)  # Adjust the value to control the head pitch(will receive the coordintes from supervisor)

class NaoRobot:
    def __init__(self):
        self.robot = Robot()
        self.detector = NaoSoccerBallDetector(self.robot)
        self.time_step = int(self.robot.getBasicTimeStep())

        # Initialize motion and forward motion file
        self.motion = self.robot.getDevice('Motion')
        self.forwards = Motion('../../plugins/motions/Forwards50.motion')

        # Initialize left and right motors
        self.left_motor = self.robot.getDevice('LAnklePitch')
        self.right_motor = self.robot.getDevice('RAnklePitch')

        # Check if motor devices were successfully initialized
        if self.left_motor is None or self.right_motor is None:
            print("Error: Failed to initialize motor devices.")
        else:
            # Set position and velocity for motors
            self.left_motor.setPosition(float('inf'))
            self.right_motor.setPosition(float('inf'))
            self.left_motor.setVelocity(0.0)
            self.right_motor.setVelocity(0.0)

        # Load kicking motion file
        self.kick_motion = Motion('../../plugins/motions/Shoot.motion')

        self.kp_linear = 0.1  # Proportional control gain for linear velocity
        self.kp_angular = 0.1  # Proportional control gain for angular velocity

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

    def walk_forward(self):
        self.forwards.play()

    def stop_walk(self):
        self.forwards.stop()

    def kick_ball(self):
        self.kick_motion.play()

    def run(self):
        while self.robot.step(self.time_step) != -1:
            ball_position = self.detector.detect_soccer_ball()
            goal_position = (5, 5, 5)  # Assuming the goal post's position is fixed
            
            if ball_position:
                print("Attacker Detected Soccer Ball Position:", ball_position)
                self.navigate_to_goal_post(ball_position, goal_position)
                self.walk_forward()  # Start walking forward
                # Check if ball is in kicking range and trigger kick
                if self.is_in_kick_range(ball_position):
                    self.kick_ball()
            else:
                print("Soccer ball not detected.")
                self.stop_walk()  # Stop walking if ball is not detected

    def is_in_kick_range(self, ball_position):
        # Will add logic to check if the ball is in kicking range
        # Return True if the ball is in range, False otherwise
        return False 

if __name__ == "__main__":
    nao_robot = NaoRobot()
    nao_robot.run()
