import os
import time
import logging
import threading


from flask import Flask, render_template
from github import Github

app = Flask(__name__)

# Initialize GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOS = os.getenv("GITHUB_REPOS").split(",")

if GITHUB_TOKEN:
    gh = Github(GITHUB_TOKEN)
else:
    gh = Github()

# Global variable to store GitHub data
latest_data = {
    "milestones": [],
    "issues": [],
    "pull_requests": [],
    "issues_count": 0,
    "pull_requests_count": 0,
}


# Background task to update GitHub data every 90 seconds
def fetch_github_data():
    global latest_data

    app.logger.info("Starting github scheduled.")
    while True:
        milestones_data = []
        issues_data = []
        pr_data = []

        for repo_name in GITHUB_REPOS:
            app.logger.debug(f"Processing {repo_name}")
            repo = gh.get_repo(repo_name)

            # Fetch milestones
            milestones = repo.get_milestones(state="open")
            for milestone in milestones:
                milestones_data.append(
                    {
                        "name": milestone.title,
                        "repo_name": repo_name,
                        "progress": (
                            (
                                milestone.closed_issues
                                / (milestone.closed_issues + milestone.open_issues)
                                * 100
                            )
                            if (milestone.closed_issues + milestone.open_issues) > 0
                            else 0
                        ),
                        "issues": milestone.open_issues,
                    }
                )

            # Fetch open issues
            issues = repo.get_issues(state="open")
            for issue in issues:
                if issue.pull_request:  # Skip PRs in issues
                    continue
                issues_data.append(
                    {
                        "number": issue.number,
                        "repo_name": repo_name.split("/")[1],
                        "title": issue.title,
                        "user": issue.user.login,
                        "assignee": (
                            issue.assignee.login if issue.assignee else "Unassigned"
                        ),
                        "additions": 0,
                        "deletions": 0,
                    }
                )

            # Fetch open pull requests
            pull_requests = repo.get_pulls(state="open")
            for pr in pull_requests:
                pr_details = repo.get_pull(pr.number)
                pr_data.append(
                    {
                        "number": pr.number,
                        "repo_name": repo_name.split("/")[1],
                        "title": pr.title,
                        "user": pr.user.login,
                        "additions": pr_details.additions,
                        "deletions": pr_details.deletions,
                    }
                )

        latest_data = {
            "milestones": milestones_data,
            "issues": issues_data,
            "pull_requests": pr_data,
            "issues_count": len(issues_data),
            "pull_requests_count": len(pr_data),
        }

        app.logger.info(
            f"GitHub data updated successfully, {len(issues_data)} issues and {len(pr_data)} pull requests."
        )
        time.sleep(90)  # Wait 90 seconds before refreshing


# Start background thread for data fetching
updater_thread = threading.Thread(target=fetch_github_data)
updater_thread.daemon = True
updater_thread.start()


@app.route("/")
def index():
    return render_template(
        "index.html",
        milestones=latest_data["milestones"],
        issues=latest_data["issues"],
        issues_count=latest_data["issues_count"],
        pull_requests=latest_data["pull_requests"],
        pull_requests_count=latest_data["pull_requests_count"],
    )


if __name__ == "__main__":
    app.logger.basicConfig(level=DEBUG)
    app.run(host="0.0.0.0", port=5000)


# For WSGI
def create_app():
    return app
