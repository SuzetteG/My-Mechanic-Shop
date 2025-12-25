from flask import Blueprint

customers_bp = Blueprint('customers', __name__)

# Import routes at the end to avoid circular import issues
from . import routes

