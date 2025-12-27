from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields
from app.models import ServiceTicket, Mechanic

class MechanicMiniSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Mechanic
		load_instance = False
	id = auto_field()
	first_name = auto_field()
	last_name = auto_field()
	email = auto_field()

class ServiceTicketSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = ServiceTicket
		load_instance = True
		include_fk = True
	mechanics = fields.List(fields.Nested(MechanicMiniSchema), dump_only=True)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
