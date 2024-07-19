from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__, template_folder="templates")


@admin_bp.route("/")
def admin_index():
    return render_template("admin/index.html")
