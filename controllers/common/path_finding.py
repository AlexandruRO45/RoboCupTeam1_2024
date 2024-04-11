import numpy as np


class PotentialFieldPathfinding:
    def __init__(self, robot_position, goal_position, obstacle_positions, other_player_positions):
        self.robot_position = np.array(robot_position)
        self.goal_position = np.array(goal_position)
        self.obstacle_positions = np.array(obstacle_positions)
        self.other_player_positions = np.array(other_player_positions)

        self.k_att = 0.5  # Attractive force coefficient
        self.k_rep = 2.0  # Repulsive force coefficient
        self.d_rep = 1.0  # Repulsion distance threshold
        self.max_force = 1.0  # Maximum force magnitude

    def attractive_force(self):
        # Compute attractive force towards the goal
        direction = self.goal_position - self.robot_position
        distance = np.linalg.norm(direction)
        if distance == 0:
            return np.zeros_like(direction)
        return self.k_att * direction / distance

    def repulsive_force(self):
        # Compute repulsive force from obstacles and other players
        repulsive_force = np.zeros_like(self.robot_position)
        for obstacle_position in np.vstack((self.obstacle_positions, self.other_player_positions)):
            direction = self.robot_position - obstacle_position
            distance = np.linalg.norm(direction)
            if distance < self.d_rep:
                repulsive_force += self.k_rep * (1 / distance - 1 / self.d_rep) * (1 / distance ** 2) * direction
        return repulsive_force

    def compute_force(self):
        # Compute resultant force and limit its magnitude
        attractive_force = self.attractive_force()
        repulsive_force = self.repulsive_force()
        total_force = attractive_force + repulsive_force
        magnitude = np.linalg.norm(total_force)
        if magnitude > self.max_force:
            total_force *= self.max_force / magnitude
        return total_force

    def update_position(self):
        # Update robot's position based on the computed force
        force = self.compute_force()
        self.robot_position += force

    def find_path(self, max_iterations=100, tolerance=0.01):
        # Find path using potential field algorithm
        for _ in range(max_iterations):
            prev_position = self.robot_position.copy()
            self.update_position()
            if np.linalg.norm(self.robot_position - prev_position) < tolerance:
                break
        return self.robot_position


class Robot:
    def __init__(self, position):
        self.position = np.array(position)

    def kick_ball(self, ball_position, force):
        # Simulate kicking the ball with given force towards the target position
        direction = ball_position - self.position
        distance = np.linalg.norm(direction)
        if distance == 0:
            return np.zeros_like(direction)
        return force * direction / distance


# # Example usage:
# robot_position =  # get the robot position
# ball_position =  # get the ball position
# obstacle_positions =  # get the obstacle position
# other_player_positions =  # get the other player positions
# pathfinder = PotentialFieldPathfinding(robot_position, goal_position, obstacle_positions, other_player_positions)
# final_position = pathfinder.find_path()
# print("Final robot position:", final_position)

# # After reaching the ball position, robot kicks the ball towards the goal
# robot = Robot(final_position)
# ball_position =  # get the ball position
# kick_force = 2.0  # set kick force accordingly
# kick_direction = robot.kick_ball(ball_position, kick_force)
# print("Kick direction:", kick_direction)
