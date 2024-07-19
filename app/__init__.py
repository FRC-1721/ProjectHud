import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import get_config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)

    from .admin import admin_bp
    from .dashboard import dashboard_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    with app.app_context():
        if os.getenv("FLASK_ENV") == "production":
            # Automatically apply migrations in production
            from flask_migrate import upgrade

            upgrade()

    return app
