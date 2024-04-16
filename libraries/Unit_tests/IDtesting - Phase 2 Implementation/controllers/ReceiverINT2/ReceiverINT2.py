
# chan1
# Robot controller script for NAO2 (strong based)
from controller import Robot, Receiver

# Initialize the robot
robot = Robot()
receiver = robot.getDevice("receiver")  # access the node
receiver.enable(64)

# Main loop
while robot.step(128) != -1:
    # Receive data from NAO chan1
    
    received_data_string = receiver.getString()
    print(received_data_string)

    # Process the received data (must be a comma-separated string)
    received_numbers = [float(num) for num in received_data_string.split(",")]
    print(type(received_numbers))
  

    # Check if data was received
    if len(received_numbers) == 5:
        s, t, x, y, z = received_numbers
        print(f"Received 4D coordinates: ({s}, {t}, {x}, {y}, {z})")
        print (received_numbers)
        print(type(received_numbers))
        print(received_numbers[0])
        if received_numbers[0] ==0:
            print("aha2!")
            ball_coords= received_numbers[-3:]  # from here, try the method of sending 3, 4, 5 or 6 coords to be filtered in case of multiple send commands
            print(ball_coords)
    elif len(received_numbers) == 3:
        q, r, t= received_numbers
        print(f"Received 3D coordinates: ({q}, {r}, {t})")
        print (received_numbers)
         
        goal_coords= received_numbers # from here, try the method of sending 3, 4, 5 or 6 coords to be filtered in case of multiple send commands
        print(goal_coords)

    else:
        print("Invalid or no data received.")
        
        receiver.nextPacket()
    