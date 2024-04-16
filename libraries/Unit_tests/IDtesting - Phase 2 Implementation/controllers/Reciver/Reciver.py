
# chan1
# Robot controller script for NAO2 (strong based)
from controller import Robot, Receiver

# Initialize the robot
robot = Robot()
receiver = robot.getDevice("receiver")  # access the node
receiver.enable(64)

# Main loop
while robot.step(64) != -1:
    # Receive data from NAO chan1
    
    received_data_string = receiver.getString()
    print(received_data_string)

    # Process the received data (must be a comma-separated string)
    received_numbers = [float(num) for num in received_data_string.split(",")]
    print(type(received_numbers))

    # Check if data was received
    if len(received_numbers) == 3:
        x, y, z = received_numbers
        print(f"Received 3D coordinates: ({x}, {y}, {z})")
        print (received_numbers)
        print(type(received_numbers))
    else:
        print("Invalid or no data received.")
        
        receiver.nextPacket()
    
        
