from datetime import datetime
from ..extensions import db

# Junction table for many-to-many relationship between ServiceTicket and Mechanic
service_ticket_mechanics = db.Table(
    "service_ticket_mechanics",
    db.Column("service_ticket_id", db.Integer, db.ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanics.id"), primary_key=True),
)

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    service_tickets = db.relationship(
        "ServiceTicket",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    salary  = db.Column(db.Numeric(10, 2), nullable=True)
    service_tickets = db.relationship(
        "ServiceTicket",
        secondary=service_ticket_mechanics,
        back_populates="mechanics"
    )

class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    vin = db.Column(db.String(17), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Numeric(10, 2), nullable=True)
    service_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    customer = db.relationship("Customer", back_populates="service_tickets")
    mechanics = db.relationship(
        "Mechanic",
        secondary=service_ticket_mechanics,
        back_populates="service_tickets"
    )
