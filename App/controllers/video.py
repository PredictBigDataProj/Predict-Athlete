
from .user import create_user
from .regular import create_regular
import joblib 
import os
from App.database import db
import csv
from datetime import datetime
from App.models import Player
from App.default_config import STATIC_PATH

from flask import Flask, Response, render_template
from ultralytics import YOLO
import cv2
import numpy as np
from collections import deque
import math

#READ ME IM IMPORTANT!!!!!

#Now That i have your attention, look at the notebook. It explains this better. :)


image_model = YOLO("yolov8n.pt")

video_path = os.path.join(STATIC_PATH, 'videos', 'Final-Penalty.mp4')

print (video_path)

# video_path = "/static/videos/Final-Penalty.mp4"
cap = cv2.VideoCapture(video_path)

display_width = 960
display_height = 540

GOAL_TOP_LEFT = (550, 450)
GOAL_BOTTOM_RIGHT = (1310, 690)

ball_positions = []
ball_history = deque(maxlen=5)

total_attempts = 0
goals_scored = 0

frames_since_lost = 0
max_lost_frames = 5

kick_detected = False
kick_speed_threshold = 15


def is_goal(ball_center, goal_tl, goal_br):
    x, y = ball_center
    x1, y1 = goal_tl
    x2, y2 = goal_br
    return x1 <= x <= x2 and y1 <= y <= y2


def calculate_speed(p1, p2):
    if p1 is None or p2 is None:
        return 0
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def generate_frames():
    global total_attempts, goals_scored, frames_since_lost, kick_detected
    print("[DEBUG] generate_frames called")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Frame not captured")
            # break
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        print("[DEBUG] Frame captured")
        # Draw goal box
        cv2.rectangle(frame, GOAL_TOP_LEFT, GOAL_BOTTOM_RIGHT, (255, 0, 0), 2)

        results = image_model(frame)

        ball_detected = False
        ball_center = None
        speed = 0

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                label = image_model.names[cls_id]
                conf = box.conf[0]

                if label == "sports ball":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    ball_positions.append((center_x, center_y))

                    ball_detected = True
                    ball_center = (center_x, center_y)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, ball_center, 5, (0, 0, 255), -1)
                    cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if ball_detected:
            ball_history.append(ball_center)
            frames_since_lost = 0

            if len(ball_history) >= 2:
                speed = calculate_speed(ball_history[-2], ball_history[-1])
                if speed > 300:
                    speed = 0

            if speed > kick_speed_threshold and not kick_detected:
                total_attempts += 1
                kick_detected = True
                print("Kick detected!")

            if is_goal(ball_center, GOAL_TOP_LEFT, GOAL_BOTTOM_RIGHT):
                if goals_scored < total_attempts:
                    goals_scored += 1
                    cv2.putText(frame, "GOAL!", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        else:
            frames_since_lost += 1
            if frames_since_lost > max_lost_frames:
                kick_detected = False
                ball_history.clear()

        if ball_detected:
            speed_text = f"Speed: {speed:.2f}"
            cv2.putText(frame, speed_text, (ball_center[0], ball_center[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        else:
            cv2.putText(frame, "Speed: 0.00", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.putText(frame, f"Attempts: {total_attempts}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Goals: {goals_scored}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        for i in range(1, len(ball_positions)):
            cv2.line(frame, ball_positions[i-1], ball_positions[i], (255, 0, 0), 2)

 
        resized_frame = cv2.resize(frame, (display_width, display_height))
        ret, buffer = cv2.imencode('.jpg', resized_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')