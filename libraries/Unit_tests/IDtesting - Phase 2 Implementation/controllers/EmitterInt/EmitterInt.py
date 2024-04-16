from controller import Robot, Supervisor, Emitter

# Initialize the robot
robot = Supervisor()
emitter = robot.getDevice("emitter")  # Get the emitter node

#======= BLOCKS TO ADD HERE =======#

# Call the coordinates of all robots
# Call the coordinates of the target
# Call 

ball = robot.getFromDef("BALL")
ball_tran= ball.getField('translation')
ball_pos= ball_tran.getSFVec3f()
print (f" BALL'S POSITION IS {ball_pos}")
print(f" {ball_pos[2]}")

ROB_A= robot.getFromDef("A")
ROB_B= robot.getFromDef("B")
Rob_C= robot.getFromDef("C")

ball_tran= ball.getField('translation')
ball_pos= ball_tran.getSFVec3f()
ball_tran= ball.getField('translation')
ball_pos= ball_tran.getSFVec3f()
ball_tran= ball.getField('translation')
ball_pos= ball_tran.getSFVec3f()



# Create data lists
data_to_send_1 = [2, 3, 0.3, 5, 3 , 0.3, 1, 2, 0.3]
data_to_send_2 = [3, 2, -1, 0.35]

# Convert data lists to comma-separated strings
data_strings = [
    ",".join(str(num) for num in data_to_send_1),
    ",".join(str(num) for num in data_to_send_2),
    ]

# Send each data string in a loop
for data_string in data_strings:
    emitter.send(data_string.encode())

# Main simulation loop
while robot.step(64) != -1:
    # Your other code here (if needed)
    
    pass

# Cleanup
robot.cleanup()
#conclusion : SEND COMMAND MUST BE LOOPED
#OR CONSIDER SENDING A LARGE ARRAY/LIST and INDEX THEM [x,y,z, q,r,t,etc..