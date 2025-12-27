from flask import Flask
from config import ProductionConfig, Config
from app.extensions import db, limiter, cache
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp
from app.blueprints.inventory import inventory_bp
from app.swagger import swagger_bp

def create_app(config_class=Config):
        with app.app_context():
            from app import models  # Ensure models are imported so tables are created
            db.create_all()
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(swagger_bp)

    return app

app = create_app(ProductionConfig)
