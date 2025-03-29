from flask import Flask, request, jsonify, render_template
import cv2
import torch
import os
import psycopg2
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO("yolov8n.pt")  

conn = psycopg2.connect(
    dbname="yoloObject",
    user="postgres",
    password="nafizml",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS detections (
        id SERIAL PRIMARY KEY,
        video_name TEXT,
        timestamp FLOAT,
        object_class TEXT,
        confidence FLOAT,
        bbox_x1 FLOAT,
        bbox_y1 FLOAT,
        bbox_x2 FLOAT,
        bbox_y2 FLOAT
    )
""")
conn.commit()

def process_video(video_name, video_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = fps * 15  
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0:
            results = model(frame)  
            
            for result in results:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box.tolist()
                    cursor.execute("""
                        INSERT INTO detections (video_name, timestamp, object_class, confidence, bbox_x1, bbox_y1, bbox_x2, bbox_y2)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (video_name, frame_count / fps, model.names[int(cls)], conf, x1, y1, x2, y2))
            conn.commit()
        
        frame_count += 1
    
    cap.release()

@app.route("/detect", methods=["POST"])
def detect():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video_file = request.files["video"]
    video_path = "temp_video.mp4"
    video_file.save(video_path)
    
    process_video(video_file.filename, video_path)
    os.remove(video_path)
    
    return jsonify({"message": "Detection results saved to database"})

@app.route("/results")
def results():
    cursor.execute("SELECT video_name, timestamp, object_class, confidence, bbox_x1, bbox_y1, bbox_x2, bbox_y2 FROM detections ORDER BY timestamp DESC")
    data = cursor.fetchall()
    return render_template("results.html", detections=data)

if __name__ == "__main__":
    app.run(debug=True)
