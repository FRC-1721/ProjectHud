import os
from flask import current_app as app
from flask import Blueprint, jsonify, render_template

#from app.services.github_service import GitHubService

screens_bp = Blueprint("screens", __name__)


@screens_bp.route("/api/screens")
def get_screens():
    screens = ["/table"]

#    try:
#        if len(app.github_service.latest_data["pending_reviews"]) > 0:
#            screens.append("/pending")
#    except:
#        pass

    if os.getenv("COUNT_DOWN"):
        screens.append("/countdown")

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
        <h1>ProjectHUD Starting! Version {os.getenv('GIT_COMMIT', 'Unknown')}</h1>
    </body>
    </html>
    """


@screens_bp.route("/pending")
def pending_screen():
    return render_template(
        "pending.html",
        **app.github_service.latest_data,
        last_updated=app.github_service.last_updated,
    )


@screens_bp.route("/table")
def table_screen():
    return render_template(
        "table.html",
        **app.github_service.latest_data,
        last_updated=app.github_service.last_updated,
    )


@screens_bp.route("/countdown")
def countdown():
    countdown_env = os.getenv("COUNT_DOWN", "0:Unknown Event")
    timestamp, event_name = countdown_env.split(":", 1)

    try:
        target_time = int(timestamp)
    except ValueError:
        target_time = 0  # Fallback if invalid

    return render_template(
        "countdown.html", target_time=target_time, event_name=event_name
    )
