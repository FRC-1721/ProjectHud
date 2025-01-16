import os
import threading

from flask import Flask

from app.routes.index import index_bp
from app.routes.screens import screens_bp

from app.services.github_service import GitHubService


app = Flask(__name__)

# Add globals
app.jinja_env.globals.update(enumerate=enumerate)


def create_app():
    # Register Blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(screens_bp)

    # Initialize GitHubService
    username_mapping = {
        pair.split(":")[0]: pair.split(":")[1]
        for pair in os.getenv("USERNAME_MAP", "").split(",")
        if ":" in pair
    }

    # Register service with app
    app.github_service = GitHubService(
        token=os.getenv("GITHUB_TOKEN"),
        repos=os.getenv("GITHUB_REPOS", "").split(","),
        username_mapping=username_mapping,
    )

    threading.Thread(target=app.github_service.fetch_data, daemon=True).start()

    return app
