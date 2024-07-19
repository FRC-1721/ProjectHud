from flask import Blueprint, render_template
from app.models import Project, Note, Task
from app import socketio
from flask_socketio import emit

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")


@dashboard_bp.route("/")
def dashboard_index():
    projects = Project.query.all()
    return render_template("dashboard/index.html", projects=projects)


@socketio.on("connect")
def handle_connect():
    emit("message", {"data": "Connected"})


@socketio.on("update")
def handle_update(data):
    project_id = data["project_id"]
    notes = Note.query.filter_by(project_id=project_id).all()
    tasks = Task.query.filter_by(project_id=project_id).all()
    emit(
        "update",
        {
            "project_id": project_id,
            "notes": [note.content for note in notes],
            "tasks": [task.description for task in tasks],
        },
        broadcast=True,
    )
