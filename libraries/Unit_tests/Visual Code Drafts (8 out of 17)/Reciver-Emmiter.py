# reciever/emmiter
from controller import Robot, Emitter, Receiver

robot = Robot()
emitter = robot.getEmitter("emitter")  # Replace with actual emitter name
receiver = robot.getReceiver("receiver")  # Create a new receiver

while robot.step(TIME_STEP) != -1:
    # Read GPS and IMU values (replace with actual sensor readings)
    gps_values = [1.23, 4.56, 7.89]
    imu_values = [0.12, 0.34, 0.56]

    # Create a message with GPS and IMU data
    message = f"{gps_values[0]} {gps_values[1]} {gps_values[2]} {imu_values[0]} {imu_values[1]} {imu_values[2]}"

    # Send the message via the emitter
    emitter.send(message)

    # Receive messages from the supervisor
    if receiver.getQueueLength() > 0:
        received_message = receiver.getData().decode("utf-8")
        receiver.nextPacket()

        # Parse the received message (assuming space-separated values)
        supervisor_gps_values = list(map(float, received_message.split()))

        # Update Robot B's GPS coordinates (replace with your logic)
        # For example:
        gps_values = supervisor_gps_values

#=========================#
        
        #supervisor reciever and emitter

    from controller import Supervisor, Receiver, Emitter

supervisor = Supervisor()
receiver = supervisor.getReceiver("receiver")  # Replace with actual receiver name
supervisor_emitter = supervisor.getEmitter("supervisor_emitter")  # Create a new emitter

while supervisor.step(TIME_STEP) != -1:
    # Receive messages from Robot B
    if receiver.getQueueLength() > 0:
        received_message = receiver.getData().decode("utf-8")
        receiver.nextPacket()

        # Parse the received message (assuming space-separated values)
        robot_b_gps_values = list(map(float, received_message.split()))

        # Process the received data (e.g., update supervisor's state)
        # For example:
        updated_gps_values = [robot_b_gps_values[0] + 0.1, robot_b_gps_values[1] - 0.2, robot_b_gps_values[2] + 0.3]

        # Send updated GPS coordinates back to Robot B
        supervisor_emitter.send(f"{updated_gps_values[0]} {updated_gps_values[1]} {updated_gps_values[2]}")


#=====================#
        
    #supervisor sender only
        from controller import Robot, Emitter

robot = Robot()
emitter = robot.getEmitter("emitter")  # Replace with actual emitter name

while robot.step(TIME_STEP) != -1:
    # Read updated GPS coordinates (replace with your logic)
    updated_gps_values = [1.23, 4.56, 7.89]

    # Create a message with updated GPS coordinates
    message = f"{updated_gps_values[0]} {updated_gps_values[1]} {updated_gps_values[2]}"

    # Send the message via the emitter
    emitter.send(message)


#========================== #
    # Robot C reciever 

    from controller import Robot, Receiver

robot = Robot()
receiver = robot.getReceiver("receiver")  # Replace with actual receiver name

while robot.step(TIME_STEP) != -1:
    # Receive messages from the supervisor
    if receiver.getQueueLength() > 0:
        received_message = receiver.getData().decode("utf-8")
        receiver.nextPacket()

        # Parse the received message (assuming space-separated values)
        supervisor_gps_values = list(map(float, received_message.split()))

        # Process the received data (e.g., update Robot C's state)
        # For example:
        robot_c_gps_values = supervisor_gps_values
        print(f"Received GPS from supervisor: {robot_c_gps_values}")


#================#
        #Sender

        from controller import Robot, Emitter

robot = Robot()
emitter = robot.getEmitter("emitter")  # Replace with actual emitter name

# Example array (replace with your data)
my_array = [1.23, 4.56, 7.89, 10.0]

while robot.step(TIME_STEP) != -1:
    # Convert the array to a space-separated string
    message = " ".join(map(str, my_array))

    # Send the message via the emitter
    emitter.send(message)


# Reciever
    
    from controller import Robot, Receiver

robot = Robot()
receiver = robot.getReceiver("receiver")  # Replace with actual receiver name

while robot.step(TIME_STEP) != -1:
    # Receive messages from the supervisor
    if receiver.getQueueLength() > 0:
        received_message = receiver.getData().decode("utf-8")
        receiver.nextPacket()

        # Parse the received message into an array
        try:
            received_array = list(map(float, received_message.split()))
            print(f"Received array from supervisor: {received_array}")

            # Perform vector/array calculations using received_array
            # For example:
            sum_of_elements = sum(received_array)
            print(f"Sum of elements: {sum_of_elements}")
        except ValueError:
            print("Error parsing received message as an array of floats.")
