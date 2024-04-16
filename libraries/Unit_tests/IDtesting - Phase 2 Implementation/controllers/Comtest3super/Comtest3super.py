#This supervisor code manages the whole protocol
from controller import Supervisor, Emitter

# Supervisor initiation
robot = Supervisor()

emitter = robot.getDevice("emitter")

# Create an array of 3 numbers to send, MAKE THIS WORK IN AN IF STATMENT LOOP FOR EACH TTYPE
data_to_send_1 = [2, 4, 3, 5, 3, 5, 4, 2, 1]
data_to_send_2 = [2, 2, 5, 3]
data_to_send_3 = [3, 2, 3, 2, 2, 1] # This is the robot selector and ball coordinator, index [0] defines which robot
data_to_send_4 = [2, 4, 3, 5, 3, 5, 4, 2, 1] # consider using another channel with another supervisor

# Convert the array to a comma-separated string
data_string_1 = ",".join(str(num) for num in data_to_send_1)
data_string_2 = ",".join(str(num) for num in data_to_send_2)
data_string_3 = ",".join(str(num) for num in data_to_send_3)
data_string_4 = ",".join(str(num) for num in data_to_send_4)


# Send the data as a string
emitter.send(data_string_1.encode())
emitter.send(data_string_2.encode())
emitter.send(data_string_3.encode())
emitter.send(data_string_4.encode())

# Get a reference to the node with the specified DEF name
node_C = "C"  # Replace "XX" with DEF name
node = robot.getFromDef(node_C)
node_B = "B"  # Replace "XX" with DEF name
node = robot.getFromDef(node_B)
node_A = "A"  # Replace "XX" with DEF name
node = robot.getFromDef(node_A)
if node:
    position_C = robot.getFromDef(node_C).getPosition()
    print(f"{node_C} position: {position_C}")
    position_B = robot.getFromDef(node_B).getPosition()
    print(f"{node_B} position: {position_B}")
    position_A = robot.getFromDef(node_A).getPosition()
    print(f"{node_A} position: {position_A}")

else:
    print(f"A Node with DEF name not found.")

# Run the simulation
while robot.step(64) != -1:
    pass