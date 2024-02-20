# RoboCupTeam1_2024

## Description

Welcome to the GitHub repository of Team 1's entry for the RoboCup 2024, hosted by the University of Glasgow. This repository is dedicated to housing the software and simulations critical for our robotic soccer team's development and performance. Our work integrates advanced robotics and AI technologies to create robust, competitive soccer-playing robots.

## Project Structure

- **controllers/**: This directory contains the brain of our robots - the control logic. It includes scripts for basic movements, ball detection, pathfinding, and strategy execution. Each role on the soccer field (attacker, defender, goalkeeper) has a dedicated controller to perform its specific tasks.

- **libraries/**: Here, we store external libraries that our project depends on. This modular approach allows for easier updates and integration of new features.

- **plugins/**: This folder includes plugins and utilities for motion conversion, enabling the use of diverse motion files (.motion) within our simulation environment. Notable contents include:

  - **motions/**: A collection of predefined robot movements and behaviors, crucial for simulating realistic soccer actions.
  - **sdformat_urdf/**: Tools for converting URDF files to SDF, ensuring compatibility with our simulation tools.
  - **yolov5/**: Integration of the YOLOv5 object detection model to enhance our robots' ability to perceive and interact with their environment.

- **protos/**: Contains the Protobuf files defining the physical and visual aspects of the robots, the soccer ball, and the playing field, along with necessary textures.

- **worlds/**: Simulation environments designed to test and validate our robots' performance and strategies in a variety of conditions.

## Technologies

Our project leverages ROS 2 for robot operation orchestration and Webots for simulation. This combination offers a powerful platform for developing and testing robotic soccer strategies.

- **ROS 2 (Humble Hawksbill)**: Provides the framework for robot communication, sensor data processing, and actuator control.
- **Webots (R2023b)**: Enables accurate and realistic simulation of robot behaviors and interactions within the soccer environment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions from the robotics and AI community. Whether you're interested in improving control algorithms, enhancing the simulation environment, or devising new strategies, your input is invaluable. For more information on how to participate, please refer to our contribution guidelines.

## Team RoboCup 2024

This repository was developed by a dedicated team of individuals, each bringing their unique expertise to the project:

- **Lavis, Ethan Spencer Cymru** - Algorithms, Strategies
- **Rosa Morales, Miguel Andres** - Management/Logistics, Simulation, Computer Vision
- **Sava, Alexandru-Mihai** - Simulation, Computer Vision
- **Ramachandran, Thushara** - Algorithms, Navigation, Strategies
- **Hamo, Saleem** - Simulation, Software Developer
- **Joseph, Matilda John** - Algorithms, Navigation
- **Saif, Ahmed** - Algorithms, Simulation, Kinematics/Control

## Acknowledgements

The team expresses its thanks to our supporters, including the University of Glasgow and the broader RoboCup community, for their guidance and resources. Together, we aim to advance the field of robotics and AI through competitive sportsmanship.
