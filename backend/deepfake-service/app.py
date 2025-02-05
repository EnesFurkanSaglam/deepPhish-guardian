import os
import cv2
import numpy as np
import joblib
from flask import Flask,request,jsonify
import jwt
from functools import wraps  

app = Flask(__name__)

model = joblib.load('deepfake_model.pkl')


def extract_simple_features(video_path):
    cap = cv2.VideoCapture(video_path)
    frames_to_read = 30
    feature_list = []
    count = 0
    
    while count < frames_to_read:
        ret,frame = cap.read()
        
        if not ret:
            break
        
        mean_val = np.mean(frame)
        feature_list.append(mean_val)
        count += 1 
    
    cap.release()
    
    return [np.mean(feature_list)]


SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

def token_requrired(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return jsonify({"error":"Token missing"}),401
        
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error":"Invalid auth format"}),401
        
        token = parts[1]
        
        try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error":"Token expired"}),401
        
        except jwt.InvalidTokenError:
            return jsonify({"error":"Invalid token"}),401
        
        return f(*args,**kwargs)
    
    return decorator
            


@app.route("/detect",methods=['POST'])
@token_requrired
def detect_deepfake():
    file = request.files.get("video")
    
    if not file:
        return jsonify({"error":"No file provided"}),400
    
    file_path = "temp_video.mp4"
    file.save(file_path)
    
    features = extract_simple_features(file_path)
    pred = model.predict([features])[0]
    
    os.remove(file_path)
    
    return jsonify({"prediction":int(pred)}),200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)