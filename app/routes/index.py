import os
from flask import Blueprint, render_template

index_bp = Blueprint("main", __name__)


@index_bp.route("/")
def index():
    return render_template(
        "index.html", refresh_duration=int(os.getenv("REFRESH_DURATION", 25))
    )
