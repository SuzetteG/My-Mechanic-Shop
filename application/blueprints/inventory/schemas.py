from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ...blueprints import Inventory

class InventorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk = True