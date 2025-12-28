from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db, limiter
from app.models import Customer
from app.utils.util import encode_token
from app.blueprints.customers.schemas import LoginSchema

auth_bp = Blueprint("auth", __name__)
login_schema = LoginSchema()

@auth_bp.route("/login", methods=["POST"])
@auth_bp.route("/customers/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        creds = login_schema.load(request.json or {})
    except ValidationError as e:
        return jsonify(e.messages), 400
    email = creds["email"]
    password = creds["password"]
    customer = db.session.scalar(select(Customer).where(Customer.email == email))
    if not customer or customer.password != password:
        return jsonify({"error": "Invalid credentials"}), 401
    token = encode_token(customer.id)
    return jsonify({"token": token}), 200
