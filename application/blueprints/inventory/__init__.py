# Initialize Inventory Blueprint
from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__)

# Ensure routes are registered
from . import routes
