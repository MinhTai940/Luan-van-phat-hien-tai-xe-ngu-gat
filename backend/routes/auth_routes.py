import bcrypt
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from extensions import mongo

auth_bp = Blueprint("auth", __name__)

# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # validate
    if not data or not all(k in data for k in ["name", "email", "password", "role"]):
        return {"error": "Missing fields"}, 400

    # check email tồn tại
    if mongo.db.users.find_one({"email": data["email"]}):
        return {"error": "Email already exists"}, 400

    # hash password
    hashed_pw = bcrypt.hashpw(
        data["password"].encode("utf-8"),
        bcrypt.gensalt()
    )

    mongo.db.users.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,  # lưu dạng hash
        "role": data["role"]
    })

    return {"message": "Register success"}


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    # validate
    if not data or not all(k in data for k in ["email", "password"]):
        return {"error": "Missing email or password"}, 400

    user = mongo.db.users.find_one({"email": data["email"]})

    if not user:
        return {"error": "User not found"}, 404

    # ⚠️ SO SÁNH HASH ĐÚNG CÁCH
    if not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        user["password"]
    ):
        return {"error": "Invalid credentials"}, 401

    # tạo JWT
    token = create_access_token(identity={
        "id": str(user["_id"]),
        "role": user["role"]
    })

    return {
        "message": "Login success",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }