from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config
from extensions import mongo, jwt


# ======================
# INIT APP
# ======================
app = Flask(__name__)
app.config.from_object(Config)

# ======================
# INIT EXTENSIONS
# ======================
mongo = PyMongo(app)
jwt = JWTManager(app)

# ======================
# IMPORT ROUTES (sau này dùng)
# ======================
# ⚠️ khi chưa tạo routes thì comment lại
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.driver_routes import driver_bp
from routes.customer_routes import customer_bp

# ======================
# REGISTER BLUEPRINT (sau này mở lại)
# ======================
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(driver_bp, url_prefix="/api/driver")
app.register_blueprint(customer_bp, url_prefix="/api/customer")

# ======================
# TEST ROUTE
# ======================
@app.route("/")
def home():
    try:
        # test insert
        mongo.db.test.insert_one({"message": "Hello MongoDB"})

        # test read
        data = list(mongo.db.test.find({}, {"_id": 0}))

        return {
            "status": "MongoDB connected ✅",
            "data": data
        }

    except Exception as e:
        return {
            "status": "MongoDB error ❌",
            "error": str(e)
        }

# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(debug=True)