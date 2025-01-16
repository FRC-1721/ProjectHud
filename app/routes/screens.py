import os
from flask import current_app as app
from flask import Blueprint, jsonify, render_template, request

from app.services.github_service import GitHubService

screens_bp = Blueprint("screens", __name__)


@screens_bp.route("/api/screens")
def get_screens():
    screens = ["/test"]

    if (
        len(app.github_service.latest_data["issues"])
        + len(app.github_service.latest_data["pull_requests"])
        + len(app.github_service.latest_data["milestones"])
        > 0
    ):
        screens.append("/table")
    else:
        app.logger.warning("Not including table screen (no data)")

    if len(app.github_service.latest_data["pending_reviews"]) > 0:
        screens.append("/pending")
    else:
        app.logger.warning("Not including pending reviews (no data)")

    branch_graph = app.github_service.latest_data["branch_graph"]
    if branch_graph:
        for repo_name in branch_graph.keys():
            screens.append(f"/branch?repo={repo_name}")
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
def branch_graph():
    repo_name = request.args.get("repo")
    if not repo_name:
        return "Repository name is required", 400

    branch_graph = app.github_service.latest_data["branch_graph"]

    if repo_name not in branch_graph:
        return f"Repository '{repo_name}' not found", 404

    # Retrieve data for the specified repository
    repo_data = branch_graph[repo_name]
    if not repo_data:
        return f"No data available for repository '{repo_name}'", 404

    # Pass only the relevant repository data to the template
    repo_data = branch_graph[repo_name]
    return render_template("branch.html", repo_name=repo_name, repo_data=repo_data)
