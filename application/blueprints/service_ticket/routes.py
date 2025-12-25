from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.extensions import db, limiter
from application.blueprints.models import ServiceTicket, Mechanic
from . import service_ticket_bp
from .schemas import ServiceTicketSchema

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)

# Batch update mechanics for a service ticket
@service_ticket_bp.put("/<int:ticket_id>/edit")
def edit_ticket_mechanics(ticket_id):
    """
    PUT /service-tickets/<ticket_id>/edit
    Body:
    {
      "add_ids": [1,2],
      "remove_ids": [3]
    }

    Lets the client update mechanic assignments in one request (less chatter, simpler UI).
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    payload = request.json or {}
    add_ids = payload.get("add_ids", []) or []
    remove_ids = payload.get("remove_ids", []) or []

    # Normalize types + de-dupe
    try:
        add_ids = list({int(x) for x in add_ids})
        remove_ids = list({int(x) for x in remove_ids})
    except (TypeError, ValueError):
        return jsonify({"error": "add_ids and remove_ids must be lists of integers"}), 400

    # Pull mechanics in one query per list
    if add_ids:
        mechanics_to_add = db.session.scalars(
            select(Mechanic).where(Mechanic.id.in_(add_ids))
        ).all()
        found_add_ids = {m.id for m in mechanics_to_add}
        missing_add = sorted(list(set(add_ids) - found_add_ids))
        if missing_add:
            return jsonify({"error": "Some add_ids not found", "missing_add_ids": missing_add}), 404

        for mech in mechanics_to_add:
            if mech not in ticket.mechanics:
                ticket.mechanics.append(mech)

    if remove_ids:
        mechanics_to_remove = db.session.scalars(
            select(Mechanic).where(Mechanic.id.in_(remove_ids))
        ).all()
        found_remove_ids = {m.id for m in mechanics_to_remove}
        missing_remove = sorted(list(set(remove_ids) - found_remove_ids))
        if missing_remove:
            return jsonify({"error": "Some remove_ids not found", "missing_remove_ids": missing_remove}), 404

        for mech in mechanics_to_remove:
            if mech in ticket.mechanics:
                ticket.mechanics.remove(mech)

    db.session.commit()
    return ticket_schema.dump(ticket), 200

@service_ticket_bp.post("/")
@limiter.limit("5 per hour")
def create_service_ticket():
    try:
        ticket = ticket_schema.load(request.json or {}, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.dump(ticket), 201

@service_ticket_bp.get("/")
def get_service_tickets():
    tickets = db.session.scalars(select(ServiceTicket)).all()
    return tickets_schema.dump(tickets), 200

@service_ticket_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
@limiter.limit("10 per minute")
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned"}), 200
    ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} assigned to ticket {ticket_id}"}), 200

@service_ticket_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    if mechanic not in ticket.mechanics:
        return jsonify({"error": "Mechanic is not assigned to this ticket"}), 400
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} removed from ticket {ticket_id}"}), 200
