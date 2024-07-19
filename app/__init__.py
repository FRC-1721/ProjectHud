from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)

    from .admin import admin_bp
    from .dashboard import dashboard_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    return app
