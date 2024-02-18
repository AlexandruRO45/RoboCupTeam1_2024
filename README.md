# RoboCupTeam1_2024

## Description

This repository is designed for Team 1's participation in RoboCup 2024 from University of Glasgow, containing all necessary software and simulations. It integrates ROS 2 (Humble Hawksbill) and Webots (R2023b) for a comprehensive development and testing environment, supporting robotic soccer strategies and operations.

## Components

- **plugins/**: Contains essential plugins for ROS 2 and Gazebo integration.
  - `ros_gz_project_template`: Template for initializing ROS 2 and Gazebo projects.
  - `sdformat_urdf`: Tool for converting URDF (Unified Robot Description Format) files to SDF (Simulation Description Format), facilitating compatibility with Gazebo.
  - `yolov5`: Incorporates YOLOv5 for object detection, enhancing robot perception capabilities within the simulation environment.

- **motions/**: Directory housing motion files (.motion) that detail predefined robot movements and behaviors, vital for simulating realistic robot actions.

- **worlds/**: Includes Gazebo world files that define various simulation environments, enabling diverse testing scenarios for robot performance and strategy validation.

