from controller import Robot, Receiver

# Initialize the receiver robot
receiver_robot = Robot()
receiver_device = receiver_robot.getDevice("receiver")  # Get the receiver

# Enable the receiver
receiver_device.enable(64)

# Initialize variables
formation = None
waypoint = None

# Main loop
while receiver_robot.step(64) != -1:
    if receiver_device.getQueueLength() > 0:
        received_data_string = receiver_device.getString()
        received_numbers = [float(num) for num in received_data_string.split(",")]

        if len(received_numbers) == 9:
            s, a, j, k, v, p, x, y, z = received_numbers
            print(f"Received 4D coordinates: ({s}, {a}, {j}, {k}, {v}, {p}, {x}, {y}, {z})")
            formation = received_numbers

        elif len(received_numbers) == 3:
            q, r, t = received_numbers
            print(f"Received 3D coordinates: ({q}, {r}, {t})")
            waypoint = received_numbers

        else:
            print("Invalid or no data received.")
            
    print(f"Formation coordinates: {formation}")
    print(f"Waypoint coordinates: {waypoint}")      

        # Clear the received data from the queue
    receiver_device.nextPacket()

# Print the final values

print(f"123 Formation coordinates: {formation}")
print(f"123 Waypoint coordinates: {waypoint}")
# Cleanup
receiver_robot.cleanup()
