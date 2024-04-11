import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "robot_log.txt")
# Load the log data from the file
with open(log_file, 'r') as file:
    document_content = file.read()

# Extract the ball and goal post positions from the log data
ball_positions = []
goal_post_positions = []
ball_directions = []
for line in document_content.split('\n'):
    if line.startswith('Ball Position:'):
        ball_x, ball_y = [int(x) for x in line.split(': ')[1][1:-1].split(', ')]
        ball_positions.append((ball_x, ball_y))
    elif line.startswith('Goal Post Position:'):
        goal_x, goal_y = [int(x) for x in line.split(': ')[1][1:-1].split(', ')]
        goal_post_positions.append((goal_x, goal_y))
    elif line.startswith('Right'):
        ball_directions.append('Right')
    elif line.startswith('Left'):
        ball_directions.append('Left')

# Create the plot for ball and goal post positions
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 600)
ax.set_ylim(0, 400)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Ball and Goal Post Positions')

# Plot the ball positions
ball_x, ball_y = zip(*ball_positions)
ax.plot(ball_x, ball_y, 'bo-', label='Ball')

# Plot the goal post positions
goal_x, goal_y = zip(*goal_post_positions)
ax.plot(goal_x, goal_y, 'ro-', label='Goal Post')

# Add a legend
ax.legend()

# Create the plot for ball trajectory
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 600)
ax.set_ylim(0, 400)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Ball Trajectory')

# Plot the ball trajectory with left and right indications
for i in range(len(ball_positions)):
    if i < len(ball_directions):
        if ball_directions[i] == 'Right':
            ax.plot([ball_positions[i][0]], [ball_positions[i][1]], 'go', label='Right')
        else:
            ax.plot([ball_positions[i][0]], [ball_positions[i][1]], 'ro', label='Left')

# Add a legend
ax.legend()

# Show the plots
plt.show()