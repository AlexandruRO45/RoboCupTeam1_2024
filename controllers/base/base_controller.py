import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controller import Keyboard, Motion
from controllers.base.base_supervisor import BaseSupervisor
from controllers.models.nao_robot import NaoRobot
from controllers.utils.motion import MotionPath, MotionBase

class BaseController:
    """Base controller class for robot control."""
    RobotList = [
        # Team Red
        'red_goalkeeper', 
        'red_defender',  
        'red_sec_attacker',
        'red_main_attacker',
        # Team Blue
        'blue_goalkeeper', 
        'blue_defender',  
        'blue_sec_attacker',
        'blue_main_attacker',
    ]  # List of robot names
    goal_post_position = {
            'Team Red': {
                'left_post': [-4.5, 0, 0],   # [x, y, z]
                'right_post': [-4.5, 0, 0],  # [x, y, z]
            },
            'Team Blue': {
                'left_post': [4.5, 0, 0],    # [x, y, z]
                'right_post': [4.5, 0, 0],   # [x, y, z]
            }
        }

    def __init__(self, robot: NaoRobot):
        """Initialize the BaseController."""
        print("Initializing BaseController...")
        self._robot = robot
        self._timestep = int(robot.getBasicTimeStep())
        self._can_see_the_ball = False
        self._receiver = self._robot.getReceiver("receiver")
        self._receiver.enable(self._timestep)
        self._emitter = self._robot.getEmitter("emitter")
        self._state = 'searching'
        self.BaseSupervisor = BaseSupervisor() #this line doesn't work.. I tried but couldn't fix it
        self.k_att = 0.5  # Attractive force coefficient
        self.k_rep = 2.0  # Repulsive force coefficient
        self.d_rep = 1.0  # Repulsion distance threshold
        self.max_force = 1.0  # Maximum force magnitude
        self.robot_position = BaseSupervisor.getBallOwner() #needs to be called the supervisor
        self.goal_position = self.goal_post_position #needs to be updated from the supervisor but I have manually declared the position to avoid confuion
        self.obstacle_positions = BaseSupervisor.get_all_robot_states() #needs to be called the supervisor
        self.other_player_positions = BaseSupervisor.get_all_robot_states() #needs to be called the supervisor

        # Assign motion files to attributes
        self.handWave = Motion("../../plugins/motions/HandWave.motion")
        self.forwards = Motion("../../plugins/motions/Forwards.motion")
        self.forwardsSprint = Motion("../../plugins/motions/ForwardsSprint.motion")
        self.forwards50 = Motion("../../plugins/motions/Forwards50.motion")
        self.backwards = Motion("../../plugins/motions/Backwards.motion")
        self.shoot = Motion("../../plugins/motions/Shoot.motion")
        self.rightShoot = Motion("../../plugins/motions/RightShoot.motion")
        self.longShoot = Motion("../../plugins/motions/LongPass.motion")
        self.leftSidePass = Motion("../../plugins/motions/SidePass_Left.motion")
        self.rightSidePass = Motion("../../plugins/motions/SidePass_Right.motion")
        self.sideStepLeft = Motion("../../plugins/motions/SideStepLeft.motion")
        self.sideStepRight = Motion("../../plugins/motions/SideStepRight.motion")
        self.standUpFromFront = Motion("../../plugins/motions/StandUpFromFront.motion")
        self.standUpFromBack = Motion("../../plugins/motions/StandUpFromBack.motion")
        self.turnLeft10 = Motion("../../plugins/motions/TurnLeft10.motion")
        self.turnLeft20 = Motion("../../plugins/motions/TurnLeft20.motion")
        self.turnLeft30 = Motion("../../plugins/motions/TurnLeft30.motion")
        self.turnLeft40 = Motion("../../plugins/motions/TurnLeft40.motion")
        self.turnLeft60 = Motion("../../plugins/motions/TurnLeft60.motion")
        self.turnLeft180 = Motion("../../plugins/motions/TurnLeft180.motion")
        self.turnRight10 = Motion("../../plugins/motions/TurnRight10.motion")
        self.turnRight10_V2 = Motion("../../plugins/motions/TurnRight10_V2.motion")
        self.turnRight40 = Motion("../../plugins/motions/TurnRight40.motion")
        self.turnRight60 = Motion("../../plugins/motions/TurnRight60.motion")
        self.standInit = Motion("../../plugins/motions/StandInit.motion")

    def connect_to_supervisor(self):
        print("Connecting to the supervisor...")
        self._receiver = self._robot.getReceiver("receiver")
        self._receiver.enable(self._timestep)
        self._emitter = self._robot.getEmitter("emitter")

    
    def find_the_ball(self):
        """Search for the ball."""
        print("Searching for the ball...")
        if not self._can_see_the_ball:
            self.turnLeft10.play()
        self._can_see_the_ball = self._robot.ballDetected(
            self._robot.upperCamera, max_distance=500
        ) or self._robot.ballDetected(
            self._robot.lowerCamera, max_distance=500
        )
        if self._can_see_the_ball:
            self._state = 'tracking'
        else:
            self._state = 'searching'

    def update_the_supervisor_with_the_ball_location(self):
        """Update supervisor with ball location."""
        print("Updating supervisor with ball location...")
        if self._can_see_the_ball:
            ball_position = self._robot.getBallPosition()
            print("ball position: ",ball_position)
            if ball_position:
                message = f"ball:{ball_position[0]},{ball_position[1]},{ball_position[2]}"
                self._emitter.send(message.encode('utf-8'))
    

    def move_ball_to_goal_post(self):
        """Move the ball towards the goal post using the nearest robot."""
        print("Moving ball towards goal post...")
        ball_position = self._robot.getBallPosition()
        
        if ball_position and self.goal_post_position:
            # Find the nearest robot to the ball
            nearest_robot = None
            min_distance = float('inf')
            for robot_name in self.RobotList:
                robot_position = self.BaseSupervisor.getRobotState(robot_name)[:3]
                distance = ((ball_position[0] - robot_position[0]) ** 2 +
                            (ball_position[1] - robot_position[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_robot = robot_name

            # Command the nearest robot to move the ball towards the goal post
            if nearest_robot:
                self._robot.moveToGoalPost(nearest_robot, self.goal_post_position)


    def attractive_force(self):
        # Compute attractive force towards the goal
        direction = self.goal_position - self.robot_position
        distance = np.linalg.norm(direction)
        if distance == 0:
            return np.zeros_like(direction)
        return self.k_att * direction / distance

    def repulsive_force(self):
        # Compute repulsive force from obstacles and other players
        repulsive_force = np.zeros_like(self.robot_position)
        for obstacle_position in np.vstack((self.obstacle_positions, self.other_player_positions)):
            direction = self.robot_position - obstacle_position
            distance = np.linalg.norm(direction)
            if distance < self.d_rep:
                repulsive_force += self.k_rep * (1 / distance - 1 / self.d_rep) * (1 / distance**2) * direction
        return repulsive_force

    def compute_force(self):
        # Compute resultant force and limit its magnitude
        attractive_force = self.attractive_force()
        repulsive_force = self.repulsive_force()
        total_force = attractive_force + repulsive_force
        magnitude = np.linalg.norm(total_force)
        if magnitude > self.max_force:
            total_force *= self.max_force / magnitude
        return total_force

    def update_position(self):
        # Update robot's position based on the computed force
        force = self.compute_force()
        self.robot_position += force

    def find_path(self, max_iterations=100, tolerance=0.01):
        # Find path using potential field algorithm
        for _ in range(max_iterations):
            prev_position = self.robot_position.copy()
            self.update_position()
            if np.linalg.norm(self.robot_position - prev_position) < tolerance:
                break
        return self.robot_position
    def move_ball_to_goal_post_apf(self):
        """Move the ball towards the goal post using the artificial potential field algorithm."""
        print("Moving ball towards goal post using APF algorithm...")
        ball_position = self._robot.getBallPosition()
        if ball_position and self.goal_post_position:
            # Calculate path using APF algorithm
            self.robot_position = self.find_path()
            # Move the robot towards the calculated position
            self._robot.moveToPosition(self.robot_position)


    def run(self):
        """Main loop for robot control."""
        print("Starting main loop...")
        self.connect_to_supervisor()
        while self._robot.step(self._timestep) != -1:
            if self._state == 'searching':
                self.find_the_ball()
            elif self._state == 'tracking':
                self.update_the_supervisor_with_the_ball_location()
                # Move the ball towards the goal post using APF algorithm
                self.move_ball_to_goal_post_apf()
            elif self._state == 'executing_order':
                self.take_order()

    

