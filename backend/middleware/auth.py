from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify

def get_current_user():
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except:
        return None