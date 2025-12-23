from application.extensions import ma
from application.blueprints.models import Customers, Service_Tickets, Mechanics, Service_Tickets_Mechanics

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customers

Customer_schema = CustomerSchema()
Customers_schema = CustomerSchema(many=True)
class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tickets
        
ServiceTicket_schema = ServiceTicketSchema()
ServiceTickets_schema = ServiceTicketSchema(many=True)

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        
Mechanic_schema = MechanicSchema()
Mechanics_schema = MechanicSchema(many=True)

class ServiceTicketMechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_Tickets_Mechanics
        
ServiceTicketMechanic_schema = ServiceTicketMechanicSchema()
ServiceTicketMechanics_schema = ServiceTicketMechanicSchema(many=True)