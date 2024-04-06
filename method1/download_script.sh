#!/bin/bash

# Download MobileNetSSD_deploy.caffemodel
wget https://github.com/C-Aniruddh/realtime_object_recognition/raw/master/MobileNetSSD_deploy.caffemodel

# Download MobileNetSSD_deploy.prototxt
wget https://github.com/chuanqi305/MobileNet-SSD/raw/master/voc/MobileNetSSD_deploy.prototxt

# Install gdown
pip install gdown

# Download DashcamVdieo2_1_1.mp4 using gdown
gdown --id 1RsEqR7AN317z5cY2cC52jab49QUqSv-j --output DashcamVdieo2_1_1.mp4
