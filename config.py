import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
