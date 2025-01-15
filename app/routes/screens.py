import os
from flask import Blueprint, jsonify

screens_bp = Blueprint("screens", __name__)


@screens_bp.route("/api/screens")
def get_screens():
    return jsonify({"version": os.getenv("GIT_REVISION", None), "screens": ["/test"]})


@screens_bp.route("/test")
def test_screen():
    return "<h1 style='text-align: center; margin-top: 20%;'>Test Screen</h1>"
