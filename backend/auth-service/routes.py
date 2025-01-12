from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from models import SessionLocal, User

SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

routes_bp = Blueprint('auth', __name__)

@routes_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return jsonify({"error": "User already exists"}), 400

        user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201

@routes_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    
    if not user:
        return jsonify({"error" : "User not found"}),404
    
    if not check_password_hash(user.password_hash,password):
        return jsonify({"error" : "Invalid password"}),401
    
    payload = {
        "user_id" : user.id,
        "email" : user.email,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=2)       
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    return jsonify({"token" : token}), 200
