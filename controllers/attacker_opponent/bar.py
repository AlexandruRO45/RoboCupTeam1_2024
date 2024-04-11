import re
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "robot_log.txt")
# Read the log file and extract relevant information
with open(log_file, 'r') as file:
    lines = file.readlines()

# Initialize lists to store data
robot_adjustments = []
distances_to_goal = []

# Parse the log file
for line in lines:
    if line.startswith('Left') or line.startswith('Right'):
        robot_adjustments.append(line.strip())
    elif line.startswith('Ball Position'):
        ball_position = line.strip().split(": ")[1][1:-1]
        ball_x, ball_y = map(int, ball_position.split(','))
        goal_post_position = lines[lines.index(line) + 1].split(": ")[1]
        # Remove non-numeric characters and whitespace from goal post position
        goal_post_position = re.sub(r'[^\d,]', '', goal_post_position)
        goal_post_x, goal_post_y = map(int, goal_post_position.split(','))
        distance_to_goal = ((ball_x - goal_post_x)**2 + (ball_y - goal_post_y)**2)**0.5
        distances_to_goal.append(distance_to_goal)

# Count the frequency of robot adjustments
left_count = robot_adjustments.count('Left')
right_count = robot_adjustments.count('Right')

# Create a bar plot for robot adjustments
plt.figure(figsize=(10, 6))
bars = plt.bar(['Left', 'Right'], [left_count, right_count], color=['red', 'blue'])
plt.xlabel('Robot Adjustments')
plt.ylabel('Frequency')
plt.title('Frequency of Robot Adjustments (Left/Right)')

# Add text labels with the count on top of the bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, '%d' % int(height), ha='center', va='bottom')

plt.show()

# Calculate the distances of the ball from the goal post
distances_to_goal = [distance[0] for distance in distances_to_goal]

# Create a bar plot for distances to the goal post
plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(distances_to_goal)), distances_to_goal, color='green')
plt.xlabel('Time Step')
plt.ylabel('Distance to Goal Post')
plt.title('Distance of Ball from Goal Post over Time')

# Add text labels with the distance above the bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, '%.2f' % distances_to_goal[i], ha='center', va='bottom')

plt.show()
