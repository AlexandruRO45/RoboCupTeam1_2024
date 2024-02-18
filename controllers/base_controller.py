"""
States:
    - find the ball
    - take order
"""
from controllers.models.nao_robot import NaoRobot


class BaseController:

    def __init__(self, robot: NaoRobot):
        self._robot = robot

        self._timestep = int(robot.getBasicTimeStep())
        self._can_see_the_ball = False

    def connect_to_supervisor(self):
        pass

    def can_see_the_ball(self):
        return self._can_see_the_ball

    # Rotate until the ball is recognized
    def find_the_ball(self):
        self._can_see_the_ball = self._robot.ballDetected(
            self._robot.upperCamera, max_distance=500
        ) or self._robot.ballDetected(
            self._robot.lowerCamera, max_distance=500
        )

    def update_the_supervisor_with_the_ball_location(self):
        ball_position = self._robot.getBallPosition()
        print("Ball Position: ", ball_position)

    def take_order(self):
        while self._robot.step(self._timestep) != -1:
            self._robot.startMotion(self._robot.wipeForhead)

    def main(self):
        self.connect_to_supervisor()
