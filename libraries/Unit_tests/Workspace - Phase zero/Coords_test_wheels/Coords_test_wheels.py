from controller import Robot, Motor, GPS, InertialUnit
import math




# Monkey's instance
robot = Robot()

# Timestep (suggestion: use global settings)
timestep = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()


  
# Motion files here, including side stepping and rotation (kindly use 30 degrees)
#eftMotor = robot.getMotor('left wheel motor')
#rightMotor = robot.getMotor('right wheel motor')

leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
#testing for wheeled robot

# Initiating GPS AND IMU
gps = robot.getGPS('gps')
gps.enable(timestep)
imu = robot.getInertialUnit('inertial unit')
imu.enable(timestep)

# set the target waypoint which comes as a variable
waypoint = [5.0, 5.0, 00]  # x, z coordinates


# Loop
while robot.step(timestep) != -1:
    # getting the current position and orientation.
    position = gps.getValues()
    orientation = imu.getRollPitchYaw()
     print('[I]: print inertial unit (roll/pitch/yaw)')

    # calculating the direction to the waypoint. x,y tensor
    direction = [waypoint[0] - position[0], waypoint[2] - position[2]]

    # calculate the targeted orientation, then keep calculating the error (difference)
    desired_orientation = math.atan2(direction[1], direction[0])
    orientation_difference = desired_orientation - orientation[2]

    # set the motor speeds (wheeled) or movment (Robot) to turn towards the waypoint.
    leftMotor.setVelocity(-orientation_difference)
    rightMotor.setVelocity(orientation_difference)
    #Next step is to adjust the margin of decision toward the point, else given 
    # that the robot has low resolution of angles, else it will end up osccilation.

    # Untill if the monkey has reached the waypoint.
    if math.sqrt(direction[0]**2 + direction[1]**2) < 0.1: # magnirtuder
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break
        #Stop