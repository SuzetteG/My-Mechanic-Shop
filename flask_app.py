from flask import Flask
from config import ProductionConfig, DevelopmentConfig
from app.extensions import db, limiter, cache

from app.blueprints.customers.routes import customer_bp
from app.blueprints.mechanics.routes import mechanic_bp
from app.blueprints.service_tickets.routes import service_ticket_bp
from app.blueprints.inventory.routes import inventory_bp


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(customer_bp)
    app.register_blueprint(mechanic_bp)
    app.register_blueprint(service_ticket_bp)
    app.register_blueprint(inventory_bp)

    return app


app = create_app(ProductionConfig)

