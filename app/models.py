from . import db


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    # isActive = db.Column(db.Boolean)

    notes = db.relationship("Note", backref="project", lazy=True)
    tasks = db.relationship("Task", backref="project", lazy=True)

    def __repr__(self):
        return f"<Project {self.name}, active {self.isActive}>"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    def __repr__(self):
        return f"<Note {self.id} for project {self.project_id}>"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.description} for project {self.project_id}>"
