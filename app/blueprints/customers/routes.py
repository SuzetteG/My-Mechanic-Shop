from flask import Blueprint, request, jsonify

customers_bp = Blueprint(
    "customers",
    __name__,
    url_prefix="/customers"
)
from marshmallow import ValidationError
from sqlalchemy import select
from app.extensions import db, limiter
from app.models import Customer, ServiceTicket
from app.utils.util import encode_token, token_required
from .schemas import CustomerSchema, LoginSchema

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()

@customers_bp.get("/<int:id>")
def get_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.dump(customer), 200


@customers_bp.post("/")
def create_customer():
    data = request.get_json() or {}


    try:
        valid_data = CustomerSchema().load(data, session=db.session)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    customer = valid_data
    db.session.add(customer)
    db.session.commit()

    return CustomerSchema().dump(customer), 201

@customers_bp.get("/")
def get_customers():
    """
    Pagination:
      /customers?page=1&per_page=10
    Prevents returning huge datasets, improves performance and UX.
    """
    # Read pagination params
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return jsonify({"error": "page and per_page must be integers"}), 400

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > 100:
        per_page = 100  # safety cap

    # Total count
    from sqlalchemy import func
    total = db.session.scalar(select(func.count(Customer.id)))

    # Items
    stmt = (
        select(Customer)
        .order_by(Customer.id.asc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    customers = db.session.scalars(stmt).all()

    pages = (total + per_page - 1) // per_page if total else 0

    return customers_schema.dump(customers), 200

@customers_bp.put("/<int:id>")
def update_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    data = request.json or {}
    for field in ["first_name", "last_name", "email", "phone", "password", "dob"]:
        if field in data:
            setattr(customer, field, data[field])
    db.session.commit()
    return customer_schema.dump(customer), 200

@customers_bp.delete("/")
@token_required
def delete_customer(user_id):
    customer = db.session.get(Customer, user_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {user_id} deleted"}), 200

@customers_bp.post("/login")
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

from app.auth import token_required

@customers_bp.get("/my-tickets")
@token_required
def my_tickets(customer_id):
    # Only return tickets for the authenticated customer
    tickets = db.session.scalars(select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)).all()
    data = [
        {
            "id": t.id,
            "customer_id": t.customer_id,
            "vin": t.vin,
            "description": t.description,
            "cost": str(t.cost) if t.cost is not None else None,
            "service_date": t.service_date.isoformat(),
        }
        for t in tickets
    ]
    return jsonify(data), 200
