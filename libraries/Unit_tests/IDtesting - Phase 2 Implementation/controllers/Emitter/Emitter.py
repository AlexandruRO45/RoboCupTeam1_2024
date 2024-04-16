from controller import Robot, Emitter

# Initialize the robot
robot = Robot()
emitter = robot.getDevice("emitter")  # Get the emitter node

# Create an array of 3 numbers to send
data_to_send = [1.23, 4.56, 7.89]

# Convert the array to a comma-separated string
data_string = ",".join(str(num) for num in data_to_send)


# Send the data as a string
emitter.send(data_string.encode())  # Encode the string as bytes, decode on the other side, chan1

# Main loop
while robot.step(64) != -1:
    # ANY control logic goes here, and ahead
    pass
