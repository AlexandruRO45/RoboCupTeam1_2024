from controller import Robot
from red_goalkeeper_controller import Goalkeeper
from red_defender_controller import Defender
from red_main_attacker_controller import MainAttacker
from red_sec_attacker_controller import SecondaryAttacker

# Create the Robot instance.
robot = Robot()
# Get the Robot Name to find the role.
robot_name = robot.getName()

# Dictionary mapping robot names to controller classes
robot_controllers = {
    "red_goalkeeper": Goalkeeper,
    "red_defender": Defender,
    "red_main_attacker": MainAttacker,
    "red_sec_attacker": SecondaryAttacker
}

# Get the corresponding controller class based on robot name
robot_controller_class = robot_controllers.get(robot_name)

# Check if a matching controller class is found
if robot_controller_class:
    # Create the robot controller instance
    robot_controller = robot_controller_class(robot)
    # Run the robot controller
    robot_controller.run()
else:
    print(f"Unknown robot name: {robot_name} for the red team!")