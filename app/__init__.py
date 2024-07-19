from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from .admin import admin_bp
    from .dashboard import dashboard_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    return app
