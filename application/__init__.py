from flask import Flask
from config import Config
from .extensions import db, limiter, cache

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    # Register Blueprints
    from .blueprints.customers import customers_bp
    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import service_ticket_bp
    from .blueprints.inventory import inventory_bp
    from . import auth
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(auth.auth_bp, url_prefix='/auth')

    # Create tables
    with app.app_context():
        from .blueprints import models  # noqa: F401
        db.create_all()

    @app.get("/")
    def health():
        return {"status": "ok"}

    return app
