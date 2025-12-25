from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.blueprints.models import Mechanic

class MechanicSchema(SQLAlchemyAutoSchema):
	class Meta:
		model = Mechanic
		load_instance = True
		include_fk = True

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from application.blueprints.models import Mechanic

class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True

# Ensure no password field is present in MechanicSchema
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
