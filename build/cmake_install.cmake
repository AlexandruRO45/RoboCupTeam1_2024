# Install script for directory: /home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_box")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_cylinder")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_heightmap")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_mesh_collada")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_mesh_obj")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_mesh_scaled")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_mesh_stl")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_plane")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/geometry_sphere")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/graph_chain")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/graph_chain_non_canonical_root")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/graph_four_bar")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/graph_loop")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/graph_tree")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/graph_tree_non_canonical_root")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_ball")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_continuous")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_fixed")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_gearbox")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_prismatic")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_prismatic_no_axis")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_revolute")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_revolute2")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_revolute_axis")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_revolute_axis_in_frame")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_revolute_default_limits")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_revolute_two_joints_two_links")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_screw")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/joint_universal")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/link_inertia")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/link_light_point")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/link_multiple_collisions")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/link_multiple_visuals")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/link_sensor_imu")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/material_blinn_phong")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/material_dynamic_lights")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/model_two_models")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/model_zero_models")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_chain")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_collision")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_collision_in_frame")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_inertial")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_inertial_in_frame")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_joint")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_joint_all")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_joint_in_frame")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_link")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_link_all")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_link_in_frame")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_model")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_visual")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/models" TYPE DIRECTORY FILES "/home/alex/Documents/RoboCupTeam1_2024/plugins/sdformat_urdf/sdformat_test_files/models/pose_visual_in_frame")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sdformat_test_files/cmake" TYPE FILE FILES
    "/home/alex/Documents/RoboCupTeam1_2024/build/sdformat_test_files/sdformat_test_filesConfig.cmake"
    "/home/alex/Documents/RoboCupTeam1_2024/build/sdformat_test_files/sdformat_test_filesConfigVersion.cmake"
    "/home/alex/Documents/RoboCupTeam1_2024/build/sdformat_test_files/sdformat_test_files_functions.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/alex/Documents/RoboCupTeam1_2024/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
