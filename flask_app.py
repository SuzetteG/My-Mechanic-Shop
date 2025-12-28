from flask import Flask
from config import ProductionConfig
from app.extensions import db, limiter, cache

from app.blueprints.customers.routes import customers_bp
from app.blueprints.inventory.routes import inventory_bp
from app.blueprints.mechanics.routes import mechanic_bp
from app.blueprints.service_tickets.routes import service_tickets_bp
from app.blueprints.auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)

    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(customers_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(mechanic_bp)
    app.register_blueprint(service_tickets_bp)
    app.register_blueprint(auth_bp)

    return app

app = create_app()

