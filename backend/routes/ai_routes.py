from flask import Blueprint, request
from services.ai_service import detect_drowsiness

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/detect", methods=["POST"])
def detect():
    data = request.json

    frame = data.get("frame")
    gps = data.get("gps")

    result = detect_drowsiness(frame)

    return {
        "status": result,
        "gps": gps
    }