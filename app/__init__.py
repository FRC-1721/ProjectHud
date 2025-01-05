from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route("/")
def index():
    # Placeholder data for now
    milestones = [
        {"name": "Milestone 1", "progress": 50, "issues": 6},
        {"name": "Milestone 2", "progress": 75, "issues": 4},
    ]
    pullRequests = [
        {
            "number": 4,
            "title": "Fix the stuff",
            "user": "Joe",
            "additions": 800,
            "deletions": 599,
        }
    ]
    issues_count = 42
    pull_requests_count = 17
    latest_activity = "User X commented: 'This looks great!'"

    return render_template(
        "index.html",
        milestones=milestones,
        issues_count=issues_count,
        pull_requests_count=pull_requests_count,
        latest_activity=latest_activity,
        pull_requests=pullRequests,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
