import os
from flask import current_app as app
from flask import Blueprint, jsonify, render_template

from app.services.github_service import GitHubService

screens_bp = Blueprint("screens", __name__)


@screens_bp.route("/api/screens")
def get_screens():
    return jsonify(
        {"version": os.getenv("GIT_REVISION", None), "screens": ["/table", "/pending"]}
    )


@screens_bp.route("/test")
def test_screen():
    return f"<h1 style='text-align: center; margin-top: 20%;'>Please Wait! Version {os.getenv('GIT_REVISION', None)}</h1>"


@screens_bp.route("/pending")
def pending_screen():
    return render_template("pending.html", **app.github_service.latest_data)


@screens_bp.route("/table")
def table_screen():
    return render_template("table.html", **app.github_service.latest_data)
