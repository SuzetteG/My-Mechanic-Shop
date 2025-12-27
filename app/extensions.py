from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

db = SQLAlchemy()
ma = Marshmallow()
limiter = Limiter(key_func=get_remote_address)
cache = Cache(config={"CACHE_TYPE": "simple"})

def create_app(config_name):
    app = Flask(__name__)
    
    # Load app configuration
    app.config.from_object(f'config.{config_name}')
    
    # Import blueprints inside the function to avoid circular imports
    from .blueprints.customers import customers_bp
    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import service_ticket_bp
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/tickets')
        
    return app
