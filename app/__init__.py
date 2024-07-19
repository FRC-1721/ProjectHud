from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from config import get_config
import os

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.admin import admin_bp
    from app.dashboard import dashboard_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    with app.app_context():
        if os.getenv("FLASK_ENV") == "production":
            from flask_migrate import upgrade

            upgrade()

    return app
