from flask import Blueprint
from middleware.role import require_role

customer_bp = Blueprint("customer", __name__)

@customer_bp.route("/home")
@require_role("customer")
def customer_home():
    return {"message": "Customer access granted"}