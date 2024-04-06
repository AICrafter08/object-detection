# SSD Object Detection

This repository contains a Python script for performing object detection using Single Shot MultiBox Detector (SSD) with MobileNet architecture. It also includes a shell script for downloading the required model files and input video.

## Instructions

### Running the Shell Script

1. Download the repository or clone it to your local machine.
2. Open your terminal and navigate to the directory where the repository is located.
3. Make sure you have `wget` and `pip` installed on your system.
4. Run the following command in the terminal:

   ```bash
   ./download_script.sh
   ```

This will download the necessary model files and input video required for object detection.

### Running the Python Script

1.  Make sure you have Python installed on your system (Python 3.x recommended).
    
2.  Install the required Python dependencies using `pip`. You can install them using the following command:
    
    ```bash
    
    pip install opencv-python imutils argparse
    
    ```

3.  Once dependencies are installed, you can run the Python script using the following command:
    
    ```bash
    
    python main.py --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel --input ../DashcamVdieo2_1_1.mp4 --output cars_detection.mp4 --display 0 --use-gpu 1
    
    ```

    Make sure to replace the arguments with appropriate values according to your setup.
    
4.  The script will perform object detection on the specified input video and save the output video with detected objects.
    