class Config:
    import os

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+mysqlconnector://root:Mina0630!!!@localhost:3306/my_mechanic_shop"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    RATELIMIT_HEADERS_ENABLED = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    
    JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "300"))


