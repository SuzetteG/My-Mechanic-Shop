import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+mysqlconnector://root:Mina0630!!!@localhost:3306/my_mechanic_shop"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    RATELIMIT_HEADERS_ENABLED = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "300"))


# Production configuration
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    CACHE_TYPE = "SimpleCache"
   

