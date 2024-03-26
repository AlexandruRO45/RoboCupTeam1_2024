import os
import sys
import math 

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from controller import Supervisor

class BaseSupervisor(Supervisor):
    allowOutOfBounds = False

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

    def __init__(self):
        super().__init__()

        # Get references to devices and objects
        self.emitter = self.getDevice('emitter')
        self.ball = self.getFromDef('ball')
        self.robots = [self.getFromDef(robot) for robot in self.RobotList]

        # Initialize variables
        self.latestGoalTime = 0
        self.ballPriority = 0
        self.previousBallLocation = [0, 0, 0.0697]
        self.score = {'Team Red': 0, 'Team Blue': 0}

        # Create scoreboard labels
        self.setLabel(0, 'Score: 0 - 0', 0.4, 0.9, 0.1, 0xffffff, 0, 'Arial')

    def updateScoreboard(self):
        # Update the score display on the supervisor
        score_text = f"Score: {self.score['Team Red']} - {self.score['Team Blue']}"
        self.setLabel(0, score_text, 0.4, 0.9, 0.1, 0xffffff, 0, 'Arial')

    def isitGoal(self):
        # Check if the ball has entered a goal and update score accordingly
        for robot in self.robots:
            if robot.getBoundingBox().intersects(self.ball.getBoundingBox()):
                if robot.getField('team').getSFString() == 'red':
                    self.score['Team Blue'] += 1
                else:
                    self.score['Team Red'] += 1
                self.updateScoreboard()
                self.resetSimulation()
                break
            
    def getBallPosition(self) -> list:
        """
        Retrieves the soccer ball's coordinates on the field.
        """
        newBallLocation = self.ball.getPosition()
        if abs(newBallLocation[0]) < 4.5 and abs(newBallLocation[1]) < 4.5:
            maxDifference = max([abs(a - b) for a, b in zip(newBallLocation, self.previousBallLocation)])
            if maxDifference > 0.05:
                self.ballPriority = "N"
                self.previousBallLocation = newBallLocation
        return newBallLocation

    def setBallPosition(self, ballPosition: list) -> None:
        """
        Set the soccer ball's coordinates on the field.

        Args:
            ballPosition (list): The x, y, and z coordinates of the desired ball position.

        Raises:
            ValueError: If the ball position is outside the playable area and allowOutOfBounds is False.
        """
        if not self.allowOutOfBounds:
            x, y, z = ballPosition
            if abs(x) >= 4.5 or abs(y) >= 0.7:
                raise ValueError("Ball position is outside the playable area.")

        self.previousBallLocation = ballPosition
        translation_field = self.ball.getField("translation")
        translation_field.setSFVec3f(ballPosition)
        self.ball.resetPhysics()

    def getRobotState(self, robotName: str) -> list:
        """
        Retrieves the state (position and orientation) of a specific robot on the field.

        Args:
            robotName (str): The name of the robot to query.

        Returns:
            list: The robot's state represented as [x, y, z, roll, pitch, yaw].
        """
        robot = self.robots[robotName]
        position = robot.getPosition()
        orientation = robot.getOrientation()
        state = position + orientation
        return state

    def getBallOwner(self):
        # Calculate which team currently owns the ball based on robot distances
        ball_position = self.getBallPosition()
        min_distance = float('inf')
        ball_owner = None

        for robot_name in self.RobotList:
            robot_state = self.getRobotState(robot_name)
            robot_position = robot_state[:3]

            # Calculate distance directly within the loop
            delta_x = math.fabs(ball_position[0] - robot_position[0])
            delta_y = math.fabs(ball_position[1] - robot_position[1])
            distance = math.hypot(delta_x, delta_y)

            if distance < min_distance:
                min_distance = distance
                ball_owner = robot_name

        if ball_owner is not None:
            return "*" + ball_owner[0]
        else:
            return None

    def resetSimulation(self):
        # Reset the ball and robots to their initial positions
        self.simulationReset()
        self.setBallPosition([0, 0, 0.0697])
        for robot in self.robots:
            robot.setPosition(robot.getField("initial_position").getSFVec3f())
            robot.setOrientation(robot.getField("initial_orientation").getSFVec3f())
            robot.resetPhysics()

    def sendSupervisorData(self) -> None:
        """Send Data (ballPosition, ballOwner, ballPriority, ...) to Robots. Channel is '0'."""

        # Pack the values into a string to transmit
        message = ",".join(
            map(
                str,
                [
                    self.getTime(),
                    self.ballPriority,
                    self.getBallOwner(),
                    *self.getBallPosition(),
                    *[state for robot_name in self.RobotList for state in self.getRobotState(robot_name)],  # Unpack robot state
                ],
            )
        )

        self.emitter.send(message.encode("utf-8"))