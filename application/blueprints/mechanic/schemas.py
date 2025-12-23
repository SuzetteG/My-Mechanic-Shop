# Mechanic Marshmallow schemas will go here
from application.extensions import ma
from application.blueprints.models import Mechanics

class MechanicSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Mechanics

Mechanic_schema = MechanicSchema()
Mechanics_schema = MechanicSchema(many=True)
