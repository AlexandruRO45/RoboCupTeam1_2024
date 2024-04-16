from controller import Robot, Motor, GPS, InertialUnit
import math

# Monkey's instance
robot = Robot()

# Timestep (suggestion: use global settings)
timestep = 32

# Motion files here, including side stepping and rotation (kindly use 30 degrees)
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
$testing fro wheeled robot

# Initiating GPS AND IMU
gps = robot.getGPS('gps')
gps.enable(timestep)
imu = robot.getInertialUnit('inertial unit')
imu.enable(timestep)

# set the target waypoint which comes as a variable
waypoint = [1.0, 0.0]  # x, z coordinates


# Loop
while robot.step(timestep) != -1:
    # getting the current position and orientation.
    position = gps.getValues()
    orientation = imu.getRollPitchYaw()

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
        
        
       # =================
        
        
 # create the Supervisor instance.
supervisor = Supervisor()

# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

# get handle to the robot's translation field
robot_node = supervisor.getFromDef("MY_ROBOT")
translation_field = robot_node.getField("translation")

# main loop
while supervisor.step(timestep) != -1:
    # set new position
    new_position = [1.0, 0.0, 0.0]  # x, y, z
    translation_field.setSFVec3f(new_position)
    
    
 #    ===========
 
 from controller import Supervisor

# create the Supervisor instance.
supervisor = Supervisor()

# get the time step of the current world.
timestep = int(supervisor.getBasicTimeStep())

# get handle to the robot's translation field
robot_node = supervisor.getFromDef("MY_ROBOT")
translation_field = robot_node.getField("translation")

# get handle to the robot's controller
robot_controller = supervisor.getFromDef("MY_ROBOT_CONTROLLER")

# set the target waypoint
waypoint = [1.0, 0.0, 0.0]  # x, y, z

# main loop
while supervisor.step(timestep) != -1:
    # get the current position
    position = translation_field.getSFVec3f()

    # calculate the direction to the waypoint
    direction = [waypoint[0] - position[0], waypoint[1] - position[1], waypoint[2] - position[2]]

    # calculate the distance to the waypoint
    distance = (direction[0]**2 + direction[1]**2 + direction[2]**2)**0.5

    # if the robot is close to the waypoint, stop moving
    if distance < 0.1:
        robot_controller.setVelocity(0, 0)
    else:
        # calculate the desired speed
        speed = distance * 0.1  # for example

        # calculate the desired rotation
        rotation = math.atan2(direction[1], direction[0])  # for example

        # send the movement command to the robot's controller
        robot_controller.setVelocity(speed, rotation)
 
 
 
 # =========== Testing reciver/emmiter protocol via robot or supervisor
 
 from controller import Robot, Motor, Receiver

# creation of instance
robot = Robot()

# get the time step 
timestep = 32  #or 64

# motors and set target position to infinity
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# set up the receiver
receiver = robot.getReceiver('receiver')
receiver.enable(timestep)

# NEW loop
while robot.step(timestep) != -1:
    # check if a command is available
    if receiver.getQueueLength() > 0:
        # get the command
        command = receiver.getData().decode('utf-8')
        receiver.nextPacket()

        # parse the command
        speed, rotation = map(float, command.split())

        # calculate the wheel speeds in case of wheeled examples
        leftSpeed = speed - rotation
        rightSpeed = speed + rotation

        # set the motor speeds (no speed for robot, just dummy value
        leftMotor.setVelocity(leftSpeed)
        rightMotor.setVelocity(rightSpeed)
        
# the emitter HERE
emitter = supervisor.getEmitter('emitter')

# send a command
command = '1.0 0.0'  # speed, rotation
emitter.send(command.encode('utf-8'))