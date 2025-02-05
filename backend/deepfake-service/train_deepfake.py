import cv2
import numpy as np
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def extract_simple_features(video_path):
    cap = cv2.VideoCapture(video_path)
    frames_to_read = 30
    feature_list = []
    count = 0

    while count < frames_to_read:
        ret, frame = cap.read()

        if not ret:
            break

        mean_val = np.mean(frame)
        feature_list.append(mean_val)
        count += 1

    cap.release()
    return [np.mean(feature_list)]


data_path = "data/submission.csv"  
df = pd.read_csv(data_path)


df['label'] = (df['label'] >= 0.5).astype(int)

videos = df['filename'].tolist() 
labels = df['label'].tolist()  

x, y = [], []

for vid, lbl in zip(videos, labels):
    path = os.path.join("data/videos", vid)  
    if os.path.exists(path):
        feats = extract_simple_features(path)
        x.append(feats)
        y.append(lbl)
    else:
        print(f"File not found: {path}")

model = RandomForestClassifier()
model.fit(x, y)

joblib.dump(model, "deepfake_model.pkl")
print("Model trained and saved -> deepfake_model.pkl")
