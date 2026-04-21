from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from extensions  import mongo

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    mongo.db.users.insert_one({
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "role": data["role"]   # admin / driver / customer
    })

    return {"message": "Register success"}

# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = mongo.db.users.find_one({"email": data["email"]})

    if not user or user["password"] != data["password"]:
        return {"error": "Invalid credentials"}, 401

    token = create_access_token(identity={
        "id": str(user["_id"]),
        "role": user["role"]
    })

    return {"token": token}