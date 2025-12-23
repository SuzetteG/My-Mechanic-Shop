from flask import Flask
from .extensions import db, ma
from .blueprints.customers import customers_bp
from .blueprints.mechanic import mechanic_bp
from .blueprints.service_ticket import service_ticket_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/tickets')
    with app.app_context():
        db.create_all()
    return app
