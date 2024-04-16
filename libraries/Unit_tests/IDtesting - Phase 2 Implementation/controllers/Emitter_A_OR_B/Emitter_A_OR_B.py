from controller import Robot, Emitter

# Initialize 
robot = Robot()
emitter = robot.getDevice("emitter")  # Get the emitter node

# DEFs
robot_A_name = "A"  
robot_B_name = "B"  

# Create an array of 3 numbers to send
data_to_send_A = [5, 4, 3]  # Data for robot A
data_to_send_B = [3, 4, 5.5]  # Data for robot B

# Convert to string
data_string_A = ",".join(str(num) for num in data_to_send_A)
data_string_B = ",".join(str(num) for num in data_to_send_B)

print(robot.getName())

# Send the data as a string based on the robot's DEF name
if robot.getFromDef == robot_A_name:
    emitter.send(data_string_A.encode())
    print(f"Sent data to {robot_A_name}: {data_string_A}")
elif robot.getFromDef == robot_B_name:
    emitter.send(data_string_B.encode())
    print(f"Sent data to {robot_B_name}: {data_string_B}")
else:
    print(f"Unknown robot with DEF name: {robot.getName()}")

# Main loop
while robot.step(64) != -1:
    # ANY control logic goes here, and ahead
    pass