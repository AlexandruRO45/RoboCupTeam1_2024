import cv2
import numpy as np

# Initialize camera 
cap = robot.getDevice(('camera')(0))

while True:
    ret, frame = cap.read() #On and reading
    # Color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([30, 50, 50])
    upper_color = np.array([60, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        ball_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(ball_contour)
        cx = int(M["m10"] / M["m00"]) # moment dictionary

        # Determine direction (left or right) by comparing it to the mid-width
        if cx < frame.shape[1] // 2:
            print("Ball is going left")
        else:
            print("Ball is going right") #then apply appropriate action

    cv2.imshow("Ball Detection", frame) # May be needed for external monitoring