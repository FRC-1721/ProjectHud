import os
from flask import current_app as app
from flask import Blueprint, jsonify, render_template

from app.services.github_service import GitHubService

screens_bp = Blueprint("screens", __name__)


@screens_bp.route("/api/screens")
def get_screens():
    screens = ["/table"]
    if len(app.github_service.latest_data["pending_reviews"]) > 0:
        screens.append("/pending")
    else:
        app.logger.warning("Not including pending reviews (no data)")

    if len(app.github_service.latest_data["branch_graph"]) > 0:
        screens.append("/branch")
    else:
        app.logger.warning("Not including branch graph (no data)")

    return jsonify({"version": os.getenv("GIT_COMMIT", None), "screens": screens})


@screens_bp.route("/test")
def test_screen():
    return f"""
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background: #222;
                color: white;
                font-family: "Courier New", Courier, monospace;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <h1>Please Wait! Version {os.getenv('GIT_COMMIT', 'Unknown')}</h1>
    </body>
    </html>
    """


@screens_bp.route("/pending")
def pending_screen():
    return render_template("pending.html", **app.github_service.latest_data)


@screens_bp.route("/table")
def table_screen():
    return render_template("table.html", **app.github_service.latest_data)


@screens_bp.route("/branch")
def branch_screen():
    return render_template("branch.html", **app.github_service.latest_data)
