import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from controller import Supervisor

class BaseSupervisor(Supervisor):
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
        self.previousBallLocation = None
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
        Sets the soccer ball's coordinates on the field.

        Args:
            ballPosition (list): The x, y, and z coordinates of the ball.
        """
        self.previousBallLocation = ballPosition
        self.ball.getField("translation").setSFVec3f(ballPosition)
        self.ball.resetPhysics()

    def getRobotPosition(self, robot_name):
        # Get the 3D coordinates of a specific robot by name
        # $PLACEHOLDER$

    def getRobotOrientation(self, robot_name):
        # Get the orientation of a specific robot by name
        # $PLACEHOLDER$

    def getBallOwner(self):
        # Calculate which team currently owns the ball based on robot distances
        # $PLACEHOLDER$

    def sendSupervisorData(self):
        # Pack and send data (ball position, owner, priority, etc.) to robots via an emitter channel
        # $PLACEHOLDER$

    def resetSimulation(self):
        # Reset the simulation and robot physics
        # $PLACEHOLDER$