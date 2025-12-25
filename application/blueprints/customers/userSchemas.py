from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from application.blueprints.models import Customer, Mechanic, ServiceTicket

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
    password = fields.String(load_only=True)
    address = fields.String(required=True)
    dob = fields.Date(required=True)

from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()

class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True
    password = fields.String(load_only=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

class ServiceTicketSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)