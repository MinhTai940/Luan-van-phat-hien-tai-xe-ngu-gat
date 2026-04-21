from flask import Blueprint
from middleware.role import require_role
from extensions  import mongo

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users")
@require_role("admin")
def get_users():
    users = list(mongo.db.users.find({}, {"password": 0}))

    for u in users:
        u["_id"] = str(u["_id"])

    return users