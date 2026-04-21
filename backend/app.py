from flask import Flask
from config import Config
from extensions import mongo, jwt
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# init extension đúng cách
mongo.init_app(app)
jwt.init_app(app)
CORS(app)

# import routes
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.driver_routes import driver_bp
from routes.customer_routes import customer_bp
from routes.ai_routes import ai_bp


app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(driver_bp, url_prefix="/api/driver")
app.register_blueprint(customer_bp, url_prefix="/api/customer")
app.register_blueprint(ai_bp, url_prefix="/api/ai")

if __name__ == "__main__":
    app.run(debug=True)