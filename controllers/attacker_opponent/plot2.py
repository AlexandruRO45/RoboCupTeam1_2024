import re
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "robot_log.txt")
# Initialize lists to store data
ball_positions = []
goal_post_positions = []
robot_adjustments = []

# Regular expression patterns to extract data
pattern_ball = r"Ball Position: \((\d+), (\d+)\)"
pattern_goal = r"Goal Post Position: \((\d+), (\d+)\)"
pattern_adjustment = r"(Left|Right)"

# Parse the log file
with open(log_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        # Extract ball position
        match_ball = re.search(pattern_ball, line)
        if match_ball:
            ball_positions.append((int(match_ball.group(1)), int(match_ball.group(2))))
        
        # Extract goal post position
        match_goal = re.search(pattern_goal, line)
        if match_goal:
            goal_post_positions.append((int(match_goal.group(1)), int(match_goal.group(2))))
        
        # Check for robot adjustments
        match_adjustment = re.search(pattern_adjustment, line)
        if match_adjustment:
            robot_adjustments.append(match_adjustment.group(1))

# Plot the trajectory
ball_x, ball_y = zip(*ball_positions)
goal_x, goal_y = zip(*goal_post_positions)

plt.figure(figsize=(10, 6))
plt.plot(ball_x, ball_y, marker='o', label='Ball Position')
plt.plot(goal_x, goal_y, marker='x', linestyle='dashed', label='Goal Post Position')

# Highlight robot adjustments
for i in range(len(robot_adjustments)):
    if robot_adjustments[i] == 'Left':
        plt.scatter(ball_x[i], ball_y[i], color='red', label='Robot Adjustment (Left)')
    elif robot_adjustments[i] == 'Right':
        plt.scatter(ball_x[i], ball_y[i], color='blue', label='Robot Adjustment (Right)')

plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Robot and Ball Trajectory')
plt.legend()
plt.grid(True)
plt.show()
