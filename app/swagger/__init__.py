import os
from flask import Blueprint, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

swagger_bp = Blueprint("swagger_bp", __name__)

# Path to swagger.yaml
SWAGGER_DIR = os.path.dirname(os.path.abspath(__file__))
SWAGGER_FILE = "swagger.yaml"

@swagger_bp.route("/swagger.yaml")
def swagger_yaml():
    return send_from_directory(SWAGGER_DIR, SWAGGER_FILE)

# Swagger UI config
SWAGGER_URL = "/docs"
API_URL = "/swagger.yaml"

swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "My_Mechanic_Shop API"
    }
)

# Attach Swagger UI to this blueprint
swagger_bp.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)
