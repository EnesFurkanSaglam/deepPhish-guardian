from flask import Flask, request, jsonify
import joblib
import os 
import jwt
from functools import wraps 

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

model = joblib.load("model.pkl")


def extract_features(url):
    length = len(url)
    num_dots = url.count('.')
    has_https = 1 if url.startswith('https') else 0
    return [length, num_dots, has_https]

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None 
        
        auth_header = request.headers.get("Authorization")
        
        if auth_header:
            parts = auth_header.split()
            
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
                
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args,**kwargs)
    
    return decorated

@app.route("/predict", methods=["POST"])
@token_required
def predict_phishing():
    data = request.json
    url = data.get("url")
    
    if not url:
        return jsonify({"error": "url is missing"}), 400
    
    features  = extract_features(url)
    pred = model.predict([features])[0]
    
    return jsonify({"label": int(pred)}),200

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=6000)
