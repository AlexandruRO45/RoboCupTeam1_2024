from controller import Robot
from red_goalkeeper_controller import Goalkeeper
from red_defender_controller import Defender
from red_main_attacker_controller import MainAttacker
from red_sec_attacker_controller import SecondaryAttacker

# Create the Robot instance.
robot = Robot()
# Get the Robot Name to find the role.
robotName = robot.getName()

# Dictionary mapping robot names to controller classes
robot_controllers = {
    "red_goalkeeper": Goalkeeper,
    "red_defender": Defender,
    "red_main_attacker": MainAttacker,
    "red_sec_attacker": SecondaryAttacker
}

# Get the corresponding controller class based on robot name
robot_controller_class = robot_controllers.get(robotName)

# Check if a matching controller class is found
if robot_controller_class:
    # Create the robot controller instance
    robotController = robot_controller_class(robot)
    # Run the robot controller
    robotController.run()
else:
    print(f"Unknown robot name: {robotName} for the red team!")
