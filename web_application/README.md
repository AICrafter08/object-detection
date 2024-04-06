Introduction
------------

This Video Analysis Web Application allows users to upload videos for processing by a pre-trained machine learning model. The application highlights unique object classes, tracks object IDs across frames, and provides a visual graph of class distribution. It's built using FastAPI for the backend, with a simple HTML/CSS/JavaScript frontend for file uploads and results display.

Getting Started
---------------

### Prerequisites

Before running the application, make sure you have the following software installed:

*   Python 3.8 or newer
*   pip (Python package installer)

### Installation

1.  Clone the repository to your local machine.
2.  Navigate to the application's root directory in a terminal.
3.  Install the required Python packages using pip:

```bash
pip install fastapi uvicorn numpy opencv-python-headless matplotlib
```

This command installs FastAPI for the web framework, Uvicorn for serving the application, and other libraries like Numpy, OpenCV, and Matplotlib for processing and analyzing videos.

Folder Structure
----------------

bashCopy code

```bash
.
├── __pycache__            # Python cache files
├── app.py                 # Backend API code
├── index.html             # Frontend webpage
├── model                  # Directory for the trained model
├── myscripts.js           # JavaScript file
├── styles.css             # CSS stylesheet
├── videos                 # Directory for video uploads and outputs
```

Running the Application
-----------------------

### Backend

Start the backend server by running:

```bash
uvicorn app:app --reload
```

The `--reload` flag enables auto-reloading of the server for development purposes.

### Frontend

1.  After starting the backend server, open `index.html` in your web browser.
2.  Use the interface to upload a video and click on the "Process" button.
3.  The application will process the video, displaying a graph of class distributions and track IDs. The processed video with annotations will be available for download or viewing directly on the webpage.

Features
--------

*   **Video Upload**: Users can easily upload video files for processing.
*   **Real-time Analysis**: The application provides real-time analysis of uploaded videos, showing unique class distributions and object tracking.
*   **Results Visualization**: Users can view and download the annotated output video alongside graphical analysis of the detected objects.

Conclusion
----------

We hope this application serves your video analysis needs effectively.