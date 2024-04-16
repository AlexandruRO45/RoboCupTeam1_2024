from controller import Robot, Supervisor, Emitter
import math

# Initialize the robot
robot = Supervisor()
emitter = robot.getDevice("emitter")  # Get the emitter node
timeStep=64
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
ROB_C= robot.getFromDef("C")

AA= ROB_A.getField('translation')
A_pos= AA.getSFVec3f()
BB= ROB_B.getField('translation')
B_pos= BB.getSFVec3f()
CC= ROB_C.getField('translation')
C_pos= CC.getSFVec3f()

print (f" Robot A {A_pos=}")
print (f" Robot B {B_pos=}")
print (f" Robot C {C_pos=}")


# Define the positions of the robots (x, y coordinates)
robot_positions = {
    "A": (A_pos[0], A_pos[1]),  # Replace with actual positions
    "B": (B_pos[0], B_pos[1]),
    "C": (C_pos[0],C_pos[1]),
}
# Function to calc the distance

    
# Function to define the active zone
def get_zone_label(x_coord):
    if -5 <= x_coord < -1.67:
        return "defense"
    elif -1.67 <= x_coord < 1.67:
        return "idle"
    elif 1.67 <= x_coord <= 5:
        return "offense"
    else:
        return "unknown"  # Handle cases outside the defined zones
        
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
  
def get_closest_robot(object_x):
    min_distance = float("inf")  # Initialize with positive infinity
    closest_robot = None

    for robot, position in robot_positions.items():
        distance = calculate_distance((object_x, 0), position)
        if distance < min_distance:
            min_distance = distance
            closest_robot = robot

    return closest_robot
    

        
object_x = ball_pos[0]  # Replace with the actual x-coordinate of the object
zone_label = get_zone_label(object_x)
closest_robot = get_closest_robot(object_x)

print(f"Object position: x = {object_x:.2f}")
print(f"Zone label: {zone_label}")

if closest_robot:
    print(f"Closest robot: {closest_robot} moves")
else:
    print("No robots detected.")

data_to_sendP_1=0
# Now handle the data_to_send_1 based on zone and closest_robot
if -5 <= ball_pos[0] < -1.67:
    if closest_robot == "A":
        data_to_send_1 = [ball_pos[0], ball_pos[1], 0.3, 5, 3, 0.3, 1, 2, 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
    elif closest_robot == "B":
        data_to_send_1 = [2, 3, 0.3, ball_pos[0], ball_pos[1], 0.3, 1, 2, 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
    elif closest_robot == "C":
        data_to_send_1 = [2, 3, 0.3, 5, 3, 0.3, ball_pos[0], ball_pos[1], 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
        # Convert data lists to comma-separated strings or use them as needed

elif -1.67 <= ball_pos[0] < 1.67:
    if closest_robot == "A":
        data_to_send_1 = [ball_pos[0], ball_pos[1], 0.3, -2, -1, 0.3, -1, -1, 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
    elif closest_robot == "B":
        data_to_send_1 = [1, 1, 0.3, ball_pos[0], ball_pos[1], 0.3, 1, 2, 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
    elif closest_robot == "C":
        data_to_send_1 = [2, 3, 0.3, 5, 3, 0.3, ball_pos[0], ball_pos[1], 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]

elif 1.67 <= ball_pos[0] <= 5:
    if closest_robot == "A":
        data_to_send_1 = [ball_pos[0], ball_pos[1], 0.3, 5, 3, 0.3, 1, 2, 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
    elif closest_robot == "B":
        data_to_send_1 = [2, 3, 0.3, ball_pos[0], ball_pos[1], 0.3, 1, 2, 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
    elif closest_robot == "C":
        data_to_send_1 = [2, 3, 0.3, 5, 3, 0.3, ball_pos[0], ball_pos[1], 0.3]
        data_to_send_2 = [3, 2, -1, 0.35]
        
# Print or use data_to_send_1 as required
print(data_to_send_1)
# Convert data lists to comma-separated strings
data_strings = [
    ",".join(str(num) for num in data_to_send_1),
    ",".join(str(num) for num in data_to_send_2),
    ]

# Send each data string in a loop
for data_string in data_strings:
    emitter.send(data_string.encode())

def calculate_slope(x1, y1, x2, y2):
 """
 Calculate the slope of a line passing through two points
 """
    return (y2 - y1) / (x2 - x1)
def check_intersection(A, B, C, D):
 """
 Check if the paths of two robots intersect.
 """
     slope_AB = calculate_slope(A[0], A[1], B[0], B[1])
     slope_CD = calculate_slope(C[0], C[1], D[0], D[1])
 # Check if slopes are equal (parallel lines)
     if slope_AB == slope_CD:
         return "Parallel paths (no intersection)"
     else:
     # Find intersection point
         x_intersection = (C[1] - A[1] + slope_AB * A[0] - slope_CD * C[0]) / (slope_AB - slope_CD)
         y_intersection = slope_AB * (x_intersection - A[0]) + A[1]
     # Check if intersection point lies within line segments AB and CD
     if A[0] <= x_intersection <= B[0] and C[0] <= x_intersection <= D[0]:
         return f"Intersection point: ({x_intersection:.2f}, {y_intersection:.2f})"
         # Send a an LED' on command
         
     else:
         return "Paths do not intersect"
# Example usage
A = (1, 2) # Point A
B = (5, 6) # Point B
C = (3, 1) # Point C
D = (7, 5) # Point D
result = check_intersection(A, B, C, D)
print(result)

# Main simulation loop
while robot.step(64) != -1:
    # THIS IS WHERE THE STUFF SHOULD BE ....STUFFED.
    
    pass

# Cleanup
robot.cleanup()
#conclusion : SEND COMMAND MUST BE LOOPED
#OR CONSIDER SENDING A LARGE ARRAY/LIST and INDEX THEM [x,y,z, q,r,t,etc..