from flask import Blueprint, render_template

index_bp = Blueprint("main", __name__)


@index_bp.route("/")
def index():
    return render_template("index.html")
