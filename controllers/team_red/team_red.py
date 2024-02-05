"""
Team Red controller.
This controller is the main controller for the team red.
It assigns the roles for each member of the team:
1 Goalkeepers
2 Defenders
1 Attacker
The roles are assigned by the supervisor. 
The supervisor can change the roles based on the game situation (strtegies).
"""



from controller import Robot

def get_robot_controller(role, robot):
    """
    Dynamically imports and returns an instance of the role-specific controller.
    """
    try:
        # Dynamically import the module based on the role
        module = __import__(role.lower(), fromlist=[role])
        # Get the class from the module and instantiate it with the robot
        class_ = getattr(module, role)
        return class_(robot)
    except ImportError as e:
        print(f"Error importing {role}: {e}")
        return None
    except AttributeError as e:
        print(f"Error accessing class {role}: {e}")
        return None

# Initialize the Robot instance
robot = Robot()
robot_name = robot.getName()

# Mapping of robot names to role names (class names)
role_mapping = {
    "RED_GK": "Goalkeeper",
    "RED_DEF_L": "DefenderLeft",
    "RED_DEF_R": "DefenderRight",
    # Default to "Forward" if the robot's name doesn't match any key
}

# Get the role name based on the robot name; default to "Forward"
role_name = role_mapping.get(robot_name, "Forward")

# Get the robot controller instance for the given role
robot_controller = get_robot_controller(role_name, robot)

if robot_controller:
    # Run the robot controller if it was successfully instantiated
    robot_controller.run()
else:
    print(f"Failed to initialize controller for role: {role_name}")














from controller import Robot

# Create the Robot instance.
robot = Robot()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Assign roles based on robot names.
# This is a simplistic way to assign roles. Adjust as needed.
robot_name = robot.getName()
if robot_name == 'Robot_GK':
    role = 'Goalkeeper'
elif robot_name in ['Robot_DF1', 'Robot_DF2']:
    role = 'Defender'
elif robot_name == 'Robot_AT':
    role = 'Attacker'
else:
    role = 'Unknown'

print(f"{robot_name} assigned role: {role}")

# You might need to get devices (motors, sensors) here based on the role
# For example:
# if role == 'Goalkeeper':
#     motor = robot.getDevice('motor_gk')
#     ds = robot.getDevice('ds_gk')
#     ds.enable(timestep)
# elif role in ['Defender', 'Attacker']:
#     # Similar device retrieval and initialization for defenders and attackers

# Main loop
while robot.step(timestep) != -1:
    # Read the sensors and perform actions based on the role
    if role == 'Goalkeeper':
        # Goalkeeper specific logic
        pass
    elif role == 'Defender':
        # Defender specific logic
        pass
    elif role == 'Attacker':
        # Attacker specific logic
        pass

    # Example sensor reading and actuator commands
    # if role != 'Unknown':
    #     val = ds.getValue()
    #     motor.setPosition(10.0)

# Exit cleanup code

