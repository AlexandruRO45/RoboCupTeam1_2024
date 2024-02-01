# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of Python controller for Nao robot.
   This demonstrates how to access sensors and actuators"""

"""This is a modified version of the original movement.py file from the Webots Nao demo.
   It has been modified to implement strategies for the Nao robot in the RoboCup competition.
   All rights belong to the original authors of the file with respect to the modifications out team made."""

import cv2
from controller import Camera

# Inside the Nao class
def processCameraImage(self, camera):
    width = camera.getWidth()
    height = camera.getHeight()
    image = camera.getImage()
    
    # Convert to OpenCV format
    image = np.frombuffer(image, np.uint8).reshape((height, width, 4))
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    
    # Detect the ball using color detection (for a red ball)
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Define range of red color in HSV
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])
    
    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask= mask)
    
    # Find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    
    # Only proceed if at least one contour was found
    if len(cnts) > 0:
        # Find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        # Only proceed if the radius meets a minimum size
        if radius > 10:
            # Draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(image, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(image, center, 5, (0, 0, 255), -1)
            
            # Now we have the center of the ball, we can use this information
            # to move the robot towards the ball
            # ... Movement logic goes here ...

    # Display the resulting frame
    cv2.imshow('Frame', image)
    cv2.waitKey(1)



