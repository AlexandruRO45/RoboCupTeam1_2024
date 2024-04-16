#Testin Supervisior

from controller import Supervisor

# Initialize the monkey
supervisor = Supervisor()

# Retrive the ball's node
ball_node = supervisor.getFromDef("BALL")

# looping
while supervisor.step(64) != -1:
    # Get dynamic position every step time (make it faster and universal)
    ball_position = ball_node.getPosition()

    # Send ball coordinates via sender/reciever
    robot1.send_message(ball_position)
    robot2.send_message(ball_position)

    # This part detects opponent's position and updates it as well (based on jersy color)
    opponent1_position = detect_opponent1_position()
    opponent2_position = detect_opponent2_position()

    # Dynamic update of position
    robot1.update_position(opponent1_position)
    robot2.update_position(opponent2_position)

    # Finally, implementing ball following function from Nao_Testing_5
    robot1.follow_ball(ball_position)
    robot2.follow_ball(ball_position)


# From here, this is the PID controller side to be replaced with Fuzzy
    
    # Using the method, replace "Sensor" here
direction_val = robot.getDevice("sensor")
sensor.enable(64)  # Enable sensor with 64ms time step

# PID constants
Kp = 0.1  # A P gain
Ki = 0.01  # I gain H
Kd = 0.05  # D gain D

# Blocks
prev_error = 0
integral = 0

# Looping
while robot.step(64) != -1:
    # position update
    direction_val = sensor.getValue()  # this " sensor" value is to be replaced with the appropriate sensor or even positional coords

    # Calculate the error
    desired_position = 0.5  # or the value
    error = desired_position - direction_val
    integral += error # Update I

    # Controller (compensator)
    control_output = Kp * error + Ki * integral + Kd * (error - prev_error)

    # Output
    left = 1.0 - control_output
    right = 1.0 + control_output

    # Try to control the velocity and rate if possible
    left = robot.getDevice("left")
    right = robot.getDevice("right")
    left.setVelocity(left)  #if possible
    right.setVelocity(right)   #if possible

    # Update the error with the new one and repeat
    prev_error = error

