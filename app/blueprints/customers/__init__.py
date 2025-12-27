from flask import Blueprint

customers_bp = Blueprint("customers_bp", __name__, url_prefix="/customers")

from . import routes  # noqa: E402,F401
