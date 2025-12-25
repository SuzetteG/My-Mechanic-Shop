from flask import Blueprint, request, jsonify, current_app
from application.blueprints.models import Customer
from application.extensions import db
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

def encode_token(customer_id: int) -> str:
    expires_minutes = current_app.config.get("JWT_EXPIRES_MINUTES", 60)
    payload = {
        "sub": customer_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing/invalid Authorization header. Use Bearer <token>"}), 401
        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            return jsonify({"error": "Token missing"}), 401
        try:
            payload = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
            customer_id = int(payload["sub"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return fn(customer_id, *args, **kwargs)
    return wrapper

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    customer = Customer.query.filter_by(email=email).first()
    if customer and customer.password == password:
        token = encode_token(customer.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
