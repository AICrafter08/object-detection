#!/bin/bash

# Install Ultralytics
pip install ultralytics

# Download and extract dataset 1
mkdir -p folder1 && curl -L "https://public.roboflow.com/ds/7DC1HUigkh?key=bZnQAQXFuo" -o folder1/roboflow.zip && unzip -d folder1 folder1/roboflow.zip && rm folder1/roboflow.zip

# Download and extract dataset 2
mkdir -p folder2 && curl -L "https://public.roboflow.com/ds/kJSM3h2MeM?key=FI4wHl2s8c" -o folder2/roboflow.zip && unzip -d folder2 folder2/roboflow.zip && rm folder2/roboflow.zip

# Run data loader
python data_loader.py

# Validate the data
yolo val model=yolov8n.pt data=/content/folder4/data.yaml

# Train YOLOv8n on COCO8 for 3 epochs
yolo train model=yolov8n.pt data=/content/folder4/data.yaml epochs=3 imgsz=640

# Export the trained model to TorchScript format
yolo export model=yolov8n.pt format=torchscript

# Perform prediction using the trained model on a sample image
yolo predict model=yolov8n.torchscript source='input.jpg'
