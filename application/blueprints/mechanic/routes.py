from . import mechanic_bp
from .schemas import Mechanic_schema, Mechanics_schema
from flask import request, jsonify
from ..models import Mechanics
from ...extensions import db
from sqlalchemy import select
from marshmallow import ValidationError

# CREATE A NEW MECHANIC
@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
	try:
		mechanic_data = Mechanic_schema.load(request.json)
	except ValidationError as e:
		return jsonify(e.messages), 400
	query = select(Mechanics).where(Mechanics.Email == mechanic_data['Email'])
	existing_mechanic = db.session.execute(query).scalars().all()
	if existing_mechanic:
		return jsonify({'Error': 'Email already exists'}), 400
	new_mechanic = Mechanics(**mechanic_data)
	db.session.add(new_mechanic)
	db.session.commit()
	return Mechanic_schema.jsonify(new_mechanic), 201

# GET ALL MECHANICS
@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
	query = select(Mechanics)
	mechanics = db.session.execute(query).scalars().all()
	return Mechanics_schema.jsonify(mechanics), 200

# GET SPECIFIC MECHANIC
@mechanic_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
	mechanic = db.session.get(Mechanics, mechanic_id)
	if mechanic:
		return Mechanic_schema.jsonify(mechanic), 200
	return jsonify({'Error': 'Mechanic not found'}), 400

# UPDATE A MECHANIC
@mechanic_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
	mechanic = db.session.get(Mechanics, mechanic_id)
	if not mechanic:
		return jsonify({'Error': 'Mechanic not found'}), 400
	try:
		mechanic_data = Mechanic_schema.load(request.json)
	except ValidationError as e:
		return jsonify(e.messages), 400
	for key, value in mechanic_data.items():
		setattr(mechanic, key, value)
	db.session.commit()
	return Mechanic_schema.jsonify(mechanic), 200

# DELETE A MECHANIC
@mechanic_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
	mechanic = db.session.get(Mechanics, mechanic_id)
	if not mechanic:
		return jsonify({'Error': 'Mechanic not found'}), 400
	db.session.delete(mechanic)
	db.session.commit()
	return jsonify({'message': f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200
