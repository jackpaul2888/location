import os
import cv2
import sqlite3
from ultralytics import YOLO
import math
from datetime import datetime

# Load the trained YOLO model
model = YOLO("/home/mundax/Projects/Location_tracking/model/yolo11n_new_saved.pt")

# Connect to SQLite database (or create it)
conn = sqlite3.connect('object_detections.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS ObjectDetections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camera_id INTEGER,
    class_id INTEGER,
    center_x REAL,
    center_y REAL,
    angle REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Function to process an image and store detections in the database
def process_image(image_path, camera_id):
    # Read an image using OpenCV
    image = cv2.imread(image_path)

    # Perform inference on the image
    results = model(image)

    # Calculate center of resized image for angle reference
    height, width, _ = image.shape
    img_center_x = width / 2
    img_center_y = height / 2

    # Process results to get bounding boxes and labels
    for result in results:
        boxes = result.boxes  # Get detected boxes
        for box in boxes:
            # Get bounding box coordinates and class ID
            x1, y1, x2, y2 = box.xyxy[0]  # Top-left and bottom-right coordinates
            class_id = int(box.cls[0])  # Class ID
            
            # Calculate the center coordinates of the bounding box
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            # Calculate angle relative to the center of the image
            angle_rad = math.atan2(center_y - img_center_y, center_x - img_center_x)
            angle_deg = math.degrees(angle_rad)

            # Insert data into database
            cursor.execute('''
                INSERT INTO ObjectDetections (camera_id, class_id, center_x, center_y, angle)
                VALUES (?, ?, ?, ?, ?)
            ''', (camera_id, class_id, center_x, center_y, angle_deg))

# Loop through all images from each camera (assuming you have six cameras)
for camera_id in range(6):
    image_path = f"/home/mundax/Projects/Location_tracking/model/data/images/train/camera_{camera_id}.jpg"
    
    if os.path.exists(image_path):
        process_image(image_path, camera_id)
    else:
        print(f"Image for camera {camera_id} does not exist.")

# Commit changes and close connection
conn.commit()
conn.close()

print("All images processed and data stored in database.")
