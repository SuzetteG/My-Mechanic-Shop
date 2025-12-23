# Service Ticket Marshmallow schemas will go here
from application.extensions import ma
from application.blueprints.models import Service_Tickets, Service_Tickets_Mechanics

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Service_Tickets
		load_instance = True
		include_fk = True

ServiceTicket_schema = ServiceTicketSchema()
ServiceTickets_schema = ServiceTicketSchema(many=True)

class ServiceTicketMechanicSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Service_Tickets_Mechanics

ServiceTicketMechanic_schema = ServiceTicketMechanicSchema()
ServiceTicketMechanics_schema = ServiceTicketMechanicSchema(many=True)
