from . import customers_bp
from .userSchemas import Customer_schema, Customers_schema
from flask import request, jsonify
from ..models import Customers
from ...extensions import db
from sqlalchemy import select
from marshmallow import ValidationError

#CREATE A NEW CUSTOMER
@customers_bp.route("/", methods=['POST'])
def create_customer():
    try:
        customer_data = Customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customers).where(Customers.Email == customer_data['Email'])
    existing_customer = db.session.execute(query).scalars().all()    
    if existing_customer:
        return jsonify({"Error": "Email already exists"}), 400
    
    new_customer = Customers(**customer_data)    
    db.session.add(new_customer)
    db.session.commit()
    return Customer_schema.jsonify(new_customer), 201

#GET ALL CUSTOMERS
@customers_bp.route('/', methods=['GET'])
def get_customers():
    query = select(Customers)
    customers = db.session.execute(query).scalars().all()

    return Customers_schema.jsonify(customers), 200

#GET SPECIFIC CUSTOMER
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    query = select(Customers)
    customers = db.session.get(Customers, customer_id)
    
    if customers:
        return Customer_schema.jsonify(customers), 200
    return jsonify({"Error": "Customer not found"}), 400

#UPDATE A CUSTOMER
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.session.get(Customers, customer_id)
    
    if not customer:
        return jsonify({"Error": "Customer not found"}), 400
    
    try:
        customer_data = Customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit()
    return Customer_schema.jsonify(customer), 200

#DELETE SPECIFIC MEMBER
@customers_bp.route("/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customers, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {customer_id}, successfully deleted.'}), 200
