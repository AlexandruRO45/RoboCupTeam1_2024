
# chan1

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
    if len(received_numbers) == 4:
        t, x, y, z = received_numbers
        print(f"Received 4D coordinates: ({t}, {x}, {y}, {z})")
        print (received_numbers)
        print(type(received_numbers))
        print(received_numbers[0])
        if received_numbers[0] ==1:
            print("aha!")
            ball_coords= received_numbers[-3:]  # from here, try the method of sending 3, 4, 5 or 6 coords to be filtered in case of multiple send commands
            print(ball_coords)
    elif len(received_numbers) == 3:
        q, r, t= received_numbers_2
        print(f"Received 3D coordinates: ({q}, {r}, {t})")
        print (received_numbers)
        print(type(received_numbers))
        print(received_numbers[0])
        
         
        goal_coords= received_numbers_2  # from here, try the method of sending 3, 4, 5 or 6 coords to be filtered in case of multiple send commands
        print(goal_coords)

    else:
        print("Invalid or no data received.")
        
        receiver.nextPacket()


##conclusion : SEND COMMAND MUST BE LOOPED
#OR CONSIDER SENDING A LARGE ARRAY/LIST and INDEX THEM [x,y,z, q,r,t,etc..