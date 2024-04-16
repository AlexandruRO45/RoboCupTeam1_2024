#Final version of motion 2

from controller import Robot, Supervisor, Node

# Initialize the Supervisor
supervisor = Supervisor()
robot = supervisor.getFromDef("EPUCK")  # Replace "EPUCK" with your robot's name
ball = supervisor.getFromDef("BALL")    # Replace "BALL" with your ball's name

# Define the fixed heading point
fixed_heading_x = 10
fixed_heading_y = 0

# Main loop
while supervisor.step(64) != -1:
    # Get the robot's current position
    robot_pos = robot.getPosition()

    # Get the ball's current position
    ball_pos = ball.getPosition()

    # Calculate the vector from the robot to the ball
    ball_to_robot = [robot_pos[0] - ball_pos[0], robot_pos[2] - ball_pos[2]]

    # Calculate the vector from the ball to the fixed heading point
    ball_to_heading = [fixed_heading_x - ball_pos[0], fixed_heading_y - ball_pos[2]]

    # Calculate the angle between the two vectors (using dot product)
    dot_product = ball_to_robot[0] * ball_to_heading[0] + ball_to_robot[1] * ball_to_heading[1]
    norm_ball_to_robot = (ball_to_robot[0]**2 + ball_to_robot[1]**2)**0.5
    norm_ball_to_heading = (ball_to_heading[0]**2 + ball_to_heading[1]**2)**0.5
    angle_rad = math.acos(dot_product / (norm_ball_to_robot * norm_ball_to_heading))

    # Determine the sign of the angle (left or right)
    cross_product = ball_to_robot[0] * ball_to_heading[1] - ball_to_robot[1] * ball_to_heading[0]
    if cross_product < 0:
        angle_rad = -angle_rad

    # Set the robot's rotation (heading)
    robot.getField("rotation").setSFRotation([0, 1, 0, angle_rad])

    # Calculate the distance to the ball
    distance = norm_ball_to_robot

    # Move the robot forward (adjust speed as needed)
    if distance > 0.1:  # A threshold to stop when close to the ball
        left_motor = robot.getMotor("left wheel motor")
        right_motor = robot.getMotor("right wheel motor")
        left_motor.setVelocity(6)  # Set desired speed
        right_motor.setVelocity(6)
    else:
        # Stop the robot when it reaches the ball
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)

supervisor.simulationQuit(0)  # End the simulation
