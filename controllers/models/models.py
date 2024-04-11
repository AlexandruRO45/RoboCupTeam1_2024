# Import required libraries
from controller import Robot
from collections import defaultdict
import cv2
import numpy as np
from ultralytics import YOLO

# Initialize the robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Enable camera
camera = robot.getDevice('CameraTop')
camera.enable(timestep)

def main():
    # Track object history
    obj_history = defaultdict(lambda: [])
    
    # Initialize YOLO model
    model = YOLO(r"../utils/best.pt")

    while robot.step(timestep) != -1:
        # Capture image from the camera
        image = camera.getImage()
        width, height = camera.getWidth(), camera.getHeight()
        
        # Convert the image to RGB format
        image = np.frombuffer(image, np.uint8).reshape((height, width, 4))
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Perform object detection and tracking
        results = model.predict(frame, device='cuda', classes=[0, 1, 2, 3], conf=0.5)
        results1 = model.track(frame, persist=True, device='cuda', tracker='bytetrack.yaml', classes=[0], conf=0.5)

        # Extract boxes, names, and track IDs
        boxes = results1[0].boxes.xywh.cpu().tolist()
        names = results1[0].names
        try:
            track_ids = results1[0].boxes.id.cpu().tolist()
        except Exception as e:
            track_ids = None
        clss = results1[0].boxes.cls.cpu().tolist()

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Plot the object tracks
        if track_ids:
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                obj_track = obj_history[track_id]
                obj_track.append((float(x), float(y)))  # x, y center point
                if len(obj_track) > 30:  # Retain 30 tracks
                    obj_track.pop(0)

                # Draw the object tracking lines
                if obj_track:
                    points = np.hstack(obj_track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)
                else:
                    continue

        # Display the annotated frame
        cv2.namedWindow('Object Tracking', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Object Tracking', 400, 300)
        cv2.imshow("Object Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
