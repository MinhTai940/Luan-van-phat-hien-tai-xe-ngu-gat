from functools import wraps
from flask import jsonify
from middleware.auth import get_current_user

def require_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_current_user()

            if not user:
                return jsonify({"error": "Unauthorized"}), 401

            if user["role"] != role:
                return jsonify({"error": "Forbidden"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator