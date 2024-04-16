"""ComTest controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    gps = robot.getDevice("gps")
    gps.enable(timestep)
    imu = robot.getDevice("inertial unit")
    imu.enable(timestep)

                


                # Loop
    while robot.step(timestep) != -1:
    # Get current position and orientation
    position = gps.getValues()
    orientation = imu.getRollPitchYaw()
            
         print(f"GPS = {pos}")    # Print the angles
         print(f"Robot 'a' IMU angles: roll={roll_a}, pitch={pitch_a}, yaw={yaw_a}")
         print(f"Robot 'b' IMU angles: roll={roll_b}, pitch={pitch_b}, yaw={yaw_b}")
                  
             #Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
