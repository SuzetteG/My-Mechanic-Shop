from flask import Blueprint

mechanics_bp = Blueprint("mechanics_bp", __name__, url_prefix="/mechanics")

from . import routes  # noqa: E402,F401
