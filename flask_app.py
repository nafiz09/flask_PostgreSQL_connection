from flask import Flask, request, jsonify
import cv2
import os
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO("yolov8n.pt")  

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = fps * 15  
    frame_count = 0
    detections = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            results = model(frame)  
            detected_objects = []
            
            for result in results:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box.tolist()
                    detected_objects.append({
                        "class": model.names[int(cls)],
                        "confidence": conf,
                        "bbox": [x1, y1, x2, y2]
                    })
            detections.append({"timestamp": frame_count / fps, "objects": detected_objects})
        
        frame_count += 1
    
    cap.release()
    return detections

@app.route("/detect", methods=["POST"])
def detect():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video_file = request.files["video"]
    video_path = "PBL_ CCTV_121.mp4"
    video_file.save(video_path)
    
    detections = process_video(video_path)
    os.remove(video_path)
    
    return jsonify({"detections": detections})

if __name__ == "__main__":
    app.run(debug=True)
