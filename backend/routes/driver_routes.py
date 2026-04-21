from flask import Blueprint
from middleware.role import require_role

driver_bp = Blueprint("driver", __name__)

@driver_bp.route("/dashboard")
@require_role("driver")
def driver_dashboard():
    return {"message": "Driver access granted"}