from flask import Flask
from config import Config
from .extensions import db, limiter, cache

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Import blueprints here to avoid circular imports
    from app.blueprints.customers import customers_bp
    from app.blueprints.inventory import inventory_bp
    from app.blueprints.mechanics import mechanic_bp
    from app.blueprints.service_tickets import service_tickets_bp
    from app.blueprints.auth import auth_bp

    app.register_blueprint(customers_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(mechanic_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(auth_bp)

    return app
