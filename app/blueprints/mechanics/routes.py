from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func
from app.extensions import db, cache
from app.models import Mechanic, ServiceTicket, service_ticket_mechanics

mechanic_bp = Blueprint(
    "mechanics",
    __name__,
    url_prefix="/mechanics"
)
from .schemas import MechanicSchema

mechanics_bp = Blueprint(
    "mechanics",
    __name__,
    url_prefix="/mechanics"
)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# GET /mechanics/most-worked
@mechanic_bp.get("/most-worked")
def mechanics_most_worked():
    """
    Returns mechanics ordered by how many tickets they've worked on (descending).
    Useful for dashboard/reporting, staffing, or "top contributors".
    """
    stmt = (
        select(
            Mechanic.id,
            Mechanic.first_name,
            Mechanic.last_name,
            Mechanic.email,
            func.count(service_ticket_mechanics.c.service_ticket_id).label("ticket_count")
        )
        .select_from(Mechanic)
        .join(service_ticket_mechanics, Mechanic.id == service_ticket_mechanics.c.mechanic_id, isouter=True)
        .group_by(Mechanic.id, Mechanic.first_name, Mechanic.last_name, Mechanic.email)
        .order_by(func.count(service_ticket_mechanics.c.service_ticket_id).desc())
    )

    rows = db.session.execute(stmt).all()

    return jsonify([
        {
            "id": r.id,
            "first_name": r.first_name,
            "last_name": r.last_name,
            "email": r.email,
            "ticket_count": int(r.ticket_count),
        }
        for r in rows
    ]), 200

@mechanic_bp.post("/")
def create_mechanic():
    try:
        mechanic = mechanic_schema.load(request.json or {}, session=db.session)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.add(mechanic)
    db.session.commit()
    cache.delete_memoized(get_mechanics)
    return mechanic_schema.dump(mechanic), 201

@mechanic_bp.get("/")
@cache.cached(timeout=60)
def get_mechanics():
    mechanics = db.session.scalars(select(Mechanic)).all()
    return mechanics_schema.dump(mechanics), 200

@mechanic_bp.put("/<int:id>")
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    data = request.json or {}
    for field in ["first_name", "last_name", "email", "phone", "address", "salary"]:
        if field in data:
            setattr(mechanic, field, data[field])
    db.session.commit()
    cache.delete_memoized(get_mechanics)
    return mechanic_schema.dump(mechanic), 200

@mechanic_bp.delete("/<int:id>")
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    cache.delete_memoized(get_mechanics)
    return jsonify({"message": f"Mechanic {id} deleted"}), 200
