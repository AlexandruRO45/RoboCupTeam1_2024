import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controller import Keyboard, Motion
from controllers.models.nao_robot import NaoRobot
from controllers.utils.motion import MotionPath, MotionBase

class BaseController:
    """Base controller class for robot control."""

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

        # Initialize motion paths
        self.motion_path = MotionPath("../../motions/")

        # Initialize motions
        for motion_name in self.motion_path.motion_files:
            motion_file = self.motion_path.get_motion_file(motion_name)
            motion_name = os.path.splitext(motion_name)[0]
            setattr(self, motion_name, MotionBase(motion_name, motion_file))

    def connect_to_supervisor(self):
        print("Connecting to the supervisor...")
        self._receiver = self._robot.getReceiver("receiver")
        self._receiver.enable(self._timestep)
        self._emitter = self._robot.getEmitter("emitter")

    def can_see_the_ball(self):
        """
        Check if the ball is visible.
        
        Returns:
            bool: True if the ball is visible, False otherwise.
        """
        print("Checking if the ball is visible...")
        # Assuming the robot has camera sensors named upperCamera and lowerCamera
        ball_visible_upper = self._robot.ballDetected(self._robot.upperCamera, max_distance=500)
        ball_visible_lower = self._robot.ballDetected(self._robot.lowerCamera, max_distance=500)
        
        # Return True if the ball is visible in either camera's view
        return ball_visible_upper or ball_visible_lower

    def find_the_ball(self):
        """Search for the ball."""
        print("Searching for the ball...")
        if not self.can_see_the_ball():
            self._robot.rotate(angle=30)  # Placeholder for rotation
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
        if self.can_see_the_ball():
            ball_position = self._robot.getBallPosition()
            message = f"ball:{ball_position[0]},{ball_position[1]},{ball_position[2]}"
            self._emitter.send(message.encode('utf-8'))

    def take_order(self):
        """Receive and execute orders from the supervisor."""
        print("Taking orders...")
        if self._receiver.getQueueLength() > 0:
            message = self._receiver.getData().decode('utf-8')
            self._receiver.nextPacket()
            # Example command parsing
            if message.startswith('move_to'):
                _, x, y = message.split(':')
                self._robot.moveTo(float(x), float(y))  # Placeholder for moveTo method
            elif message == 'kick':
                self._robot.kick()
            self._state = 'executing_order'

    def get_goal_post_location(self):
        """Get the position of the goal post from the supervisor."""
        print("Getting goal post location...")
        # Assuming the method to get the goal post position is implemented in base_supervisor.py
        goal_post_position = self._robot.getGoalPostPosition()
        if goal_post_position:
            return goal_post_position
        else:
            return None

    def move_ball_to_goal_post(self):
        """Move the ball towards the goal post using the nearest robot."""
        print("Moving ball towards goal post...")
        ball_position = self._robot.getBallPosition()
        goal_post_position = self.get_goal_post_location()
        if ball_position and goal_post_position:
            # Find the nearest robot to the ball
            nearest_robot = None
            min_distance = float('inf')
            for robot_name in self._robot.RobotList:
                robot_position = self._robot.getRobotState(robot_name)[:3]
                distance = ((ball_position[0] - robot_position[0]) ** 2 +
                            (ball_position[1] - robot_position[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_robot = robot_name

            # Command the nearest robot to move the ball towards the goal post
            if nearest_robot:
                self._robot.moveToGoalPost(nearest_robot, goal_post_position)

    def run(self):
        """Main loop for robot control."""
        print("Starting main loop...")
        self.connect_to_supervisor()
        while self._robot.step(self._timestep) != -1:
            if self._state == 'searching':
                self.find_the_ball()
            elif self._state == 'tracking':
                self.update_the_supervisor_with_the_ball_location()
                self.move_ball_to_goal_post()
            elif self._state == 'executing_order':
                self.take_order()

if __name__ == "__main__":
    # Assuming NaoRobot is initialized and passed correctly
    nao_robot = NaoRobot()  # This line is placeholder and needs actual robot initialization
    controller = BaseController(nao_robot)
    controller.run()
