import os
import sys
from abc import abstractmethod

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from controllers.models.defender import Defender
from controllers.base_controller import BaseController


class Defender:
    def __init__(self, robot):
        self.robot = robot
        # Add your defender initialization code here

    def run(self):
        # Add your defender logic here
        pass

class RedDefenderController(BaseController):

    def __init__(self):
        super().__init__(Defender())
        self.robot = Defender()

    @abstractmethod
    def main(self):
        super().main()

        while not self.can_see_the_ball():
            self.find_the_ball()

        self.update_the_supervisor_with_the_ball_location()

        self.take_order()


if __name__ == '__main__':
    controller = RedDefenderController()
    controller.main()

"""
V3 
    robot = Defender()
    gps = robot.getDevice("gps")
    gps.enable(robot.timeStep)
    imu = robot.getDevice("inertial unit")
    imu.enable(robot.timeStep)

    # set the target waypoint which comes as a variable
    waypoint = [5.0, 5.0, 00]  # x, z coordinates
    # timestep = int(robot.getBasicTimeStep())
    # Loop
    while robot.step(robot.timeStep) != -1:
        # getting the current position and orientation.
        position = gps.getValues()
        orientation = imu.getRollPitchYaw()
        print('[I]: print inertial unit (roll/pitch/yaw)')

        # calculating the direction to the waypoint. x,y tensor
        direction = [waypoint[0] - position[0], waypoint[2] - position[2]]
        print(direction)

        # calculate the targeted orientation, then keep calculating the error (difference)
        desired_orientation = math.atan2(direction[1], direction[0])
        orientation_difference = desired_orientation - orientation[2]
        distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        print(f"Target orientation = {desired_orientation}")
        print(f"Orientation Delta= {orientation_difference}")
        print(f"GPS vlaue = {gps}")
        print(f"Inertial tensor = {imu}")

        while orientation_difference > 0.5:
            robot.startMotion(robot.turnLeft60)
            print("Turn left")
            # Update orientation_difference
            orientation = imu.getRollPitchYaw()
            orientation_difference = desired_orientation - orientation[2]
            print(f"Target orientation = {desired_orientation}")
            print(f"Orientation Delta = {orientation_difference}")
            print(f"GPS vlaue = {gps}")
            print(f"Inertial tensor = {imu}")
            print(f"Distance to target= {distance}")

        while distance >= 0.1:  # Changed condition
            robot.startMotion(robot.forwards)
            print(f"Distance to target= {distance}")
            print("Approaching Target")
            # Update distance
            position = gps.getValues()
            direction = [waypoint[0] - position[0], waypoint[2] - position[2]]
            distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
            robot.startMotion(robot.forwards)


"""

"""
V2 - ball detected
def main():
    robot = Defender()
    # timestep = int(robot.getBasicTimeStep())
    while robot.step(robot.timeStep) != -1:
        # Check if a ball is detected within a certain distance in either camera
        if robot.ballDetected(robot.upperCamera, max_distance=500) or robot.ballDetected(robot.lowerCamera,
                                                                                         max_distance=500):
            # Stop walking
            print('ball detected')
            robot.forwards.stop()

            # Determine the position of the ball
            ball_position = robot.getBallPosition()

            # Perform the appropriate sidestep motion based on ball position
            if ball_position == "left":
                robot.startMotion(robot.sideStepLeft)
            elif ball_position == "right":
                robot.startMotion(robot.sideStepRight)

            # Wait for the motion to complete
            robot.step(3000)  # Adjust time as needed

            # Start walking forwards again
            robot.startMotion(robot.forwards)
        else:
            # Start walking forwards if no ball is detected
            robot.startMotion(robot.forwards)
"""
"""
V1 - Enable receiver 

# # Initialize the receiver
# receiver = robot.getReceiver("receiver")
# receiver.enable(timestep)
# receiver.setChannel(5)

# while robot.step(timestep) != -1:
#     if receiver.getQueueLength() > 0:
#         message = receiver.getString()
#         print("Message received:", message)
#         receiver.nextPacket()
"""
