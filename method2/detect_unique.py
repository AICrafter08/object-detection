import cv2
import torch
import numpy as np

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Function to calculate the Euclidean distance between two points
def distance(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

# Function to detect objects and return their details
def detect_objects(frame):
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # Extract detection results
    return detections

# Initialize video capture
cap = cv2.VideoCapture('DashcamVdieo2_1_1.mp4')
frame_count = 0
traffic_lights = []  # To store the center points of traffic lights

unique_traffic_lights_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to the correct format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect objects in the current frame
    detections = detect_objects(frame_rgb)
    
    # Process detections
    for detection in detections:
        class_id = int(detection[5])
        class_name = model.names[class_id]
        if class_name == 'traffic light':
            # Calculate the center point of the bounding box
            center_point = ((detection[0] + detection[2]) / 2, (detection[1] + detection[3]) / 2)
            
            # Check if this traffic light is new
            if all(distance(center_point, prev_point) > 100 for prev_point in traffic_lights):  # 100 is a threshold, adjust based on your video resolution and camera movement
                unique_traffic_lights_count += 1
                traffic_lights.append(center_point)
    
    frame_count += 1
    if frame_count % 60 == 0:  # Optionally, print update every 60 frames
        print(f"Up to frame {frame_count}, unique traffic lights: {unique_traffic_lights_count}")

cap.release()

# Print final unique traffic light count
print(f"Final unique traffic light count: {unique_traffic_lights_count}")
