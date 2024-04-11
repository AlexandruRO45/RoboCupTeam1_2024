import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import os

def visualize_data(log_file):
    # Extract data from log file
    ball_positions = []
    goal_post_positions = []
    distances = []
    directions = []
    track_history = defaultdict(lambda: [])

    with open(log_file, "r") as file:
        for line in file:
            if line.startswith("Ball Position:"):
                ball_x, ball_y = [float(x) for x in line.split(":")[1].strip(" ()").split(", ")]
                ball_positions.append((ball_x, ball_y))
            elif line.startswith("Goal Post Position:"):
                goal_x, goal_y = [float(x) for x in line.split(":")[1].strip("() ").split(", ")]
                goal_post_positions.append((goal_x, goal_y))
            elif line.startswith("Distance to Goal Post:"):
                distance = float(line.split(":")[1].strip())
                distances.append(distance)
            elif line.startswith("Direction to Goal Post:"):
                direction = float(line.split(":")[1].strip())
                directions.append(direction)
            elif line.startswith("Left"):
                ball_x = float(line.split(":")[1].strip())
                track_history[ball_x].append("Left")
            elif line.startswith("Right"):
                ball_x = float(line.split(":")[1].strip())
                track_history[ball_x].append("Right")

    # Create plots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # Plot ball and goal post positions
    ax1.scatter([x for x, y in ball_positions], [y for x, y in ball_positions], label="Ball")
    ax1.scatter([x for x, y in goal_post_positions], [y for x, y in goal_post_positions], label="Goal Post")
    ax1.set_title("Ball and Goal Post Positions")
    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.legend()

    # Plot ball trajectory
    track_x = []
    track_y = []
    for position, directions in track_history.items():
        for direction in directions:
            if direction == "Left":
                track_x.append(position)
                track_y.append(0)
            else:
                track_x.append(position)
                track_y.append(1)
    ax2.plot(track_x, track_y)
    ax2.set_title("Ball Trajectory")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")

    # Plot distance and direction to goal post
    ax3.plot(distances)
    ax3.set_title("Distance to Goal Post")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Distance (m)")

    ax4 = ax3.twinx()
    ax4.plot(directions, color="r")
    ax4.set_ylabel("Direction (rad)", color="r")
    ax4.tick_params(axis='y', labelcolor="r")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, "robot_log.txt")
    visualize_data(log_file)
