#!/bin/bash

# Clone the YOLOv5 repository
git clone https://github.com/ultralytics/yolov5.git
cd yolov5/

# Install dependencies
pip install -r requirements.txt

# Download YOLOv5s pre-trained weights
wget https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5s.pt

# Run object detection
python detect.py --source /content/DashcamVdieo2_1_1.mp4 --weights /content/yolov5/yolov5s.pt --img 640 --save-txt --save-conf
