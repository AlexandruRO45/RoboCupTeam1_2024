import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import math
import csv
import matplotlib.pyplot as plt

from controller import Supervisor
from models.nao_robot import NaoRobot
from base import base_controller 
from utils.data import ChartDrawer

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
        self.ball = self.getFromDef('SOCCER_BALL')
        self.robots = [self.getFromDef(robot) for robot in self.RobotList]

        # Initialize variables
        self.latestGoalTime = 0
        self.ballPriority = 0
        self.previousBallLocation = [0, 0, 0.0697]
        self.score = {'Team Red': 0, 'Team Blue': 0}

        # Create scoreboard labels
        self.setLabel(0, 'Score: 0 (RED) - 0 (BLUE)', 0.4, 0.9, 0.1, 0xffffff, 0, 'Arial')

    def updateScoreboard(self):
        # Update the score display on the supervisor
        score_text = f"Score: {self.score['Team Red']} (RED) - {self.score['Team Blue']} (BLUE)"
        self.setLabel(0, score_text, 0.4, 0.9, 0.1, 0xffffff, 0, 'Arial')

    # def isitGoal(self):
    #     # Check if the ball has entered a goal and update score accordingly
    #     if self.ball is None:
    #         print("Error: Soccer ball not found.")
    #         return

    #     for robot_node in self.robots:
    #         if robot_node is None:
    #             print("Error: Robot node not found.")
    #             continue

    #         bbox_center = robot_node.getField('bboxCenter')
    #         goal_x_min = robot_node.getField('goalXMin')
    #         goal_x_max = robot_node.getField('goalXMax')
    #         goal_y_min = robot_node.getField('goalYMin')
    #         goal_y_max = robot_node.getField('goalYMax')
    #         goal_z_min = robot_node.getField('goalZMin')
    #         goal_z_max = robot_node.getField('goalZMax')

    #         if bbox_center is None or goal_x_min is None or goal_x_max is None or goal_y_min is None \
    #                 or goal_y_max is None or goal_z_min is None or goal_z_max is None:
    #             print("Error: Missing field in robot node.")
    #             continue

    #         bbox_center_value = bbox_center.getSFVec3f()
    #         if bbox_center_value is None:
    #             print("Error: Unable to get bounding box center of the robot.")
    #             continue

    #         goal_x_min_value = goal_x_min.getSFFloat()
    #         goal_x_max_value = goal_x_max.getSFFloat()
    #         goal_y_min_value = goal_y_min.getSFFloat()
    #         goal_y_max_value = goal_y_max.getSFFloat()
    #         goal_z_min_value = goal_z_min.getSFFloat()
    #         goal_z_max_value = goal_z_max.getSFFloat()

    #         if goal_x_min_value is None or goal_x_max_value is None or goal_y_min_value is None \
    #                 or goal_y_max_value is None or goal_z_min_value is None or goal_z_max_value is None:
    #             print("Error: Unable to get goal boundaries from the robot node.")
    #             continue

    #         if self.ball.getField('bboxCenter') is None:
    #             print("Error: Soccer ball's bounding box center not found.")
    #             continue

    #         ball_bbox_center = self.ball.getField('bboxCenter').getSFVec3f()
    #         if ball_bbox_center is None:
    #             print("Error: Unable to get bounding box center of the soccer ball.")
    #             continue

    #         if ball_bbox_center[0] > goal_x_min_value and ball_bbox_center[0] < goal_x_max_value and \
    #         ball_bbox_center[1] > goal_y_min_value and ball_bbox_center[1] < goal_y_max_value and \
    #         ball_bbox_center[2] > goal_z_min_value and ball_bbox_center[2] < goal_z_max_value:
    #             if robot_node.getField('team').getSFString() == 'red':
    #                 self.score['Team Blue'] += 1
    #             else:
    #                 self.score['Team Red'] += 1
    #             self.updateScoreboard()
    #             self.resetSimulation()
    #             break

    # def isitGoal(self):
    #     # Check if the ball has entered a goal and update score accordingly
    #     for robot_node in self.robots:
    #         if self.ball.getField('bboxCenter').getSFVec3f()[0] > robot_node.getField('goalXMin').getSFFloat() and \
    #         self.ball.getField('bboxCenter').getSFVec3f()[0] < robot_node.getField('goalXMax').getSFFloat() and \
    #         self.ball.getField('bboxCenter').getSFVec3f()[1] > robot_node.getField('goalYMin').getSFFloat() and \
    #         self.ball.getField('bboxCenter').getSFVec3f()[1] < robot_node.getField('goalYMax').getSFFloat() and \
    #         self.ball.getField('bboxCenter').getSFVec3f()[2] > robot_node.getField('goalZMin').getSFFloat() and \
    #         self.ball.getField('bboxCenter').getSFVec3f()[2] < robot_node.getField('goalZMax').getSFFloat():
    #             if robot_node.getField('team').getSFString() == 'red':
    #                 self.score['Team Blue'] += 1
    #             else:
    #                 self.score['Team Red'] += 1
    #             self.updateScoreboard()
    #             self.resetSimulation()
    #             break
    #     # for robot in self.robots:
    #     #     if robot.getBoundingBox().intersects(self.ball.getBoundingBox()):
    #     #         if robot.getField('team').getSFString() == 'red':
    #     #             self.score['Team Blue'] += 1
    #     #         else:
    #     #             self.score['Team Red'] += 1
    #     #         self.updateScoreboard()
    #     #         self.resetSimulation()
    #     #         break

    def isitGoal(self):
        ball_coordinate = self.getBallPosition()

        if abs(ball_coordinate[0]) > 4.5:
            if -0.7 < ball_coordinate[1] < 0.7:  # Check if ball is within goal width
                goal_team = "RED" if ball_coordinate[0] > 4.5 else "BLUE"
                print(f"{goal_team} GOAL!")
                if goal_team == "RED":
                    self.score['Team Red'] += 1
                else:
                    self.score['Team Blue'] += 1

                self.updateScoreboard()
                self.resetSimulation()

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

    def getGameState(self):
        """
        Retrieves the current state of the game, including robot positions and ball ownership.
        """
        game_state = {}
        game_state["time_steps"] = self.getTime()
        game_state["possession"] = self.getBallOwner()
        game_state["ball_position"] = self.getBallPosition()
        game_state["RedGoalkeeper"] = self.getRobotState("red_goalkeeper")
        game_state["RedDefender"] = self.getRobotState("red_defender")
        game_state["RedSecondaryAttacker"] = self.getRobotState("red_sec_attacker")
        game_state["RedMainAttacker"] = self.getRobotState("red_main_attacker")
        game_state["BlueGoalkeeper"] = self.getRobotState("blue_goalkeeper")
        game_state["BlueDefender"] = self.getRobotState("blue_defender")
        game_state["BlueSecondaryAttacker"] = self.getRobotState("blue_sec_attacker")
        game_state["BlueMainAttacker"] = self.getRobotState("blue_main_attacker")
        
        return game_state
    
    def writeGameStateToCSV(self, filename: str, game_state: dict) -> None:
        """
        Writes the current game state to a CSV file.

        Args:
            filename (str): The name of the CSV file to write to.
            game_state (dict): The game state dictionary to write.
        """
        # Get the path to the libraries directory
        libraries_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'libraries')

        # Create the path to the new location of the CSV file
        new_csv_path = os.path.join(libraries_dir, filename)

        # Write the game state to the new CSV file
        with open(new_csv_path, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(game_state.values())

    def getRobotState(self, robotName: str) -> list:
        """
        Retrieves the state (position and orientation) of a specific robot on the field.

        Args:
            robotName (str): The name of the robot to query.

        Returns:
            list: The robot's state represented as [x, y, z, roll, pitch, yaw].
        """
        for robot_node in self.robots:
            if robot_node.getField("name").getSFString() == robotName:
                position = robot_node.getPosition()
                orientation = robot_node.getOrientation()
                state = position + orientation
                return state
        # robot = self.robots[robotName]
        # position = robot.getPosition()
        # orientation = robot.getOrientation()
        # state = position + orientation
        # return state
    
    # Hypothetical function to get all robot states in a single call (replace with your implementation)
    def get_all_robot_states(self):
        return {name: self.getRobotState(name) for name in self.RobotList}

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

    def run(self):
        """
        Handles the primary simulation loop for the RoboCup supervisor.
        """

        # Initialize variables for enhancements
        player_trajectories = {}  # Dictionary to store robot positions over time
        last_robot_states = {}     # Dictionary to store last robot states for timeout detection
        timeout_threshold = 5  # Seconds of inactivity before timeout (adjustable)

        while True:
            if self.step(32) == -1:
                break
            self.sendSupervisorData()
            self.isitGoal()
            self.updateScoreboard()

            # Track and visualize player trajectories
            current_robot_states = self.get_all_robot_states() 
            for robot_name, state in current_robot_states.items():
                position = state[:3]
                if robot_name not in player_trajectories:
                    player_trajectories[robot_name] = [position]
                else:
                    player_trajectories[robot_name].append(position)

            # Implement custom timeout mechanism
            for robot_name, state in current_robot_states.items():
                if robot_name not in last_robot_states:
                    last_robot_states[robot_name] = state
                else:
                    # Calculate distance between current and last state
                    distance = math.hypot(state[0] - last_robot_states[robot_name][0],
                                        state[1] - last_robot_states[robot_name][1])
                    if distance < 0.1:  # Threshold for insignificant movement
                        # Update timeout counter for this robot (replace with actual timeout handling)
                        print(f"Warning: Robot {robot_name} seems inactive for {timeout_threshold} seconds")
                    last_robot_states[robot_name] = state
            
            # Introduce logging system
            game_state = self.getGameState()
            self.writeGameStateToCSV("game_state_log.csv", game_state)

            # Dynamic difficulty adjustment (placeholder for future implementation)
            # ... (code to analyze score and adjust difficulty parameters)

            # Integration with external visualization tools (placeholder for future implementation)
            # ... (code to interact with extAernal visualization tools)

            # # Call controller's run method
            # print("Calling BaseController.run()...")
            # base_controller.BaseController.run()

# if __name__ == "__main__":
#     # Initialize the supervisor
#     supervisor = BaseSupervisor()
#     supervisor.run()
