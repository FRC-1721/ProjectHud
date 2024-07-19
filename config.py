import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    db_internal_ipv4 = (
        "172.19.0.3"  # Populated from docker, a local sqlite would work too
    )
    # SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://postgres:postgres@{db_internal_ipv4}/project_hud_db"
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost/project_hud_db"
    )


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
