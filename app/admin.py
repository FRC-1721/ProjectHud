from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Project, Note, Task

admin_bp = Blueprint("admin", __name__, template_folder="templates")


@admin_bp.route("/")
def admin_index():
    projects = Project.query.all()
    return render_template("admin/index.html", projects=projects)


@admin_bp.route("/add_project", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        new_project = Project(name=name, description=description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("admin.admin_index"))
    return render_template("admin/add_project.html")


@admin_bp.route("/add_note/<int:project_id>", methods=["GET", "POST"])
def add_note(project_id):
    if request.method == "POST":
        content = request.form["content"]
        new_note = Note(content=content, project_id=project_id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for("admin.admin_index"))
    return render_template("admin/add_note.html", project_id=project_id)


@admin_bp.route("/add_task/<int:project_id>", methods=["GET", "POST"])
def add_task(project_id):
    if request.method == "POST":
        description = request.form["description"]
        new_task = Task(description=description, project_id=project_id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("admin.admin_index"))
    return render_template("admin/add_task.html", project_id=project_id)
