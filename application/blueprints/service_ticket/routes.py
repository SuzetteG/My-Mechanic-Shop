from . import service_ticket_bp
from .schemas import ServiceTicket_schema, ServiceTickets_schema, ServiceTicketMechanic_schema, ServiceTicketMechanics_schema
from flask import request, jsonify
from ..models import Service_Tickets, Service_Tickets_Mechanics
from ...extensions import db
from sqlalchemy import select
from marshmallow import ValidationError

# ASSIGN MECHANIC TO SERVICE TICKET
@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
	ticket = db.session.get(Service_Tickets, ticket_id)
	if not ticket:
		return jsonify({'Error': 'Service Ticket not found'}), 404
	ticket.MechanicId = mechanic_id
	db.session.commit()
	return jsonify({'message': f'Mechanic {mechanic_id} assigned to Service Ticket {ticket_id}.'}), 200

# REMOVE MECHANIC FROM SERVICE TICKET
@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
	ticket = db.session.get(Service_Tickets, ticket_id)
	if not ticket:
		return jsonify({'Error': 'Service Ticket not found'}), 404
	if ticket.MechanicId != mechanic_id:
		return jsonify({'Error': f'Mechanic {mechanic_id} is not assigned to Service Ticket {ticket_id}.'}), 400
	ticket.MechanicId = None
	db.session.commit()
	return jsonify({'message': f'Mechanic {mechanic_id} removed from Service Ticket {ticket_id}.'}), 200


# CREATE A NEW SERVICE TICKET
@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
	try:
		ticket_data = ServiceTicket_schema.load(request.json)
	except ValidationError as e:
		return jsonify(e.messages), 400
	new_ticket = ticket_data  # Already a Service_Tickets instance
	db.session.add(new_ticket)
	db.session.commit()
	return ServiceTicket_schema.jsonify(new_ticket), 201

# GET ALL SERVICE TICKETS
@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
	query = select(Service_Tickets)
	tickets = db.session.execute(query).scalars().all()
	return ServiceTickets_schema.jsonify(tickets), 200

# GET SPECIFIC SERVICE TICKET
@service_ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_service_ticket(ticket_id):
	ticket = db.session.get(Service_Tickets, ticket_id)
	if ticket:
		return ServiceTicket_schema.jsonify(ticket), 200
	return jsonify({'Error': 'Service Ticket not found'}), 400

# UPDATE A SERVICE TICKET
@service_ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_service_ticket(ticket_id):
	ticket = db.session.get(Service_Tickets, ticket_id)
	if not ticket:
		return jsonify({'Error': 'Service Ticket not found'}), 400
	try:
		ticket_data = ServiceTicket_schema.load(request.json)
	except ValidationError as e:
		return jsonify(e.messages), 400
	for key, value in ticket_data.items():
		setattr(ticket, key, value)
	db.session.commit()
	return ServiceTicket_schema.jsonify(ticket), 200

# DELETE A SERVICE TICKET
@service_ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_service_ticket(ticket_id):
	ticket = db.session.get(Service_Tickets, ticket_id)
	if not ticket:
		return jsonify({'Error': 'Service Ticket not found'}), 400
	db.session.delete(ticket)
	db.session.commit()
	return jsonify({'message': f'Service Ticket id: {ticket_id}, successfully deleted.'}), 200
