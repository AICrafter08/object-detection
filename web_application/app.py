import cv2
import uvicorn
import shutil
import os
from pathlib import Path
from ultralytics import YOLO
from pydantic import BaseModel
from collections import defaultdict
from fastapi import FastAPI, File, UploadFile, HTTPException
from ultralytics.solutions import object_counter
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware

app = FastAPI()

# Define allowed origins, methods, and headers for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can change "*" to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific methods (e.g., ["GET", "POST"]) instead of "*"
    allow_headers=["*"],  # You can specify specific headers instead of "*"
)

class VideoPath(BaseModel):
    path: str

UPLOAD_DIRECTORY = Path("./videos")

@app.post("/upload_video/")
async def upload_video(file: UploadFile = File(...)):
    # Create the upload directory if it doesn't exist
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    
    file_location = UPLOAD_DIRECTORY / file.filename
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {"detail": "File uploaded successfully.", "path": str(file_location)}

@app.post("/count_objects/")
async def count_objects(video_path: VideoPath, output_path: VideoPath ):
    print(video_path.path)
    print(output_path.path)

    model = YOLO("./model/yolov8n.torchscript")
    cap = cv2.VideoCapture(video_path.path)
    assert cap.isOpened(), "Error reading video file"
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Define region points
    region_points = [(20, 400), (1080, 404), (1080, 360), (20, 360)]

    # Video writer
    video_writer = cv2.VideoWriter(output_path.path,
                        cv2.VideoWriter_fourcc(*'vp80'),
                        fps,
                        (w, h))

    # Init Object Counter
    counter = object_counter.ObjectCounter()
    counter.set_args(view_img=False,
                    reg_pts=region_points,
                    classes_names=model.names,
                    draw_tracks=True)

    class_track_dict = defaultdict(list)
    count = 0
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        tracks = model.track(im0, persist=True, show=False, conf=0.4, iou=0.5)

        im0 = counter.start_counting(im0, tracks)
        video_writer.write(im0)
        # Handling NoneType issue for boxes
        boxes = tracks[0].boxes.xyxy.cpu() if tracks[0].boxes is not None else []

        # Handling NoneType issue for clss
        clss = tracks[0].boxes.cls.cpu().tolist() if tracks[0].boxes is not None else []

        # Handling NoneType issue for track_ids
        track_ids = tracks[0].boxes.id.int().cpu().tolist() if tracks[0].boxes is not None and tracks[0].boxes.id is not None else []


        track_class = [[model.names[i], j] for i, j in zip(clss,track_ids)]
        [class_track_dict[model.names[i]].extend({j}) for i, j in zip(clss, track_ids) if j not in class_track_dict[model.names[i]]]
        
        # count+=1
        # if count>120:
        #     break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    
    # The actual object count can be extracted or processed differently depending on your requirement.
    # Here, for simplicity, we just return a message indicating that the process is complete.
    # You might want to modify this to return the actual count or other relevant information.
    element_counts_corrected = {class_name: len(elements) for class_name, elements in class_track_dict.items()}
    return {"detail": "Video processing completed. Object count is not directly returned in this example.",
            'trackids':class_track_dict,
            'unique_count':element_counts_corrected,
            'output_file': output_path.path}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
