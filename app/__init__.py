from flask import Flask, render_template
from github import Github
import os
import logging

app = Flask(__name__)

# Initialize GitHub API
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOS = os.getenv("GITHUB_REPOS").split(",")

if GITHUB_TOKEN:
    gh = Github(GITHUB_TOKEN)
else:
    gh = Github()


@app.route("/")
def index():
    milestones_data = []
    issues_data = []
    pr_data = []

    for repo_name in GITHUB_REPOS:
        repo = gh.get_repo(repo_name)

        # Fetch milestones
        milestones = repo.get_milestones(state="open")
        for milestone in milestones:
            milestones_data.append(
                {
                    "name": milestone.title,
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
                    "title": issue.title,
                    "user": issue.user.login,
                    "additions": 0,  # GitHub API doesn't directly provide these
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
                    "title": pr.title,
                    "user": pr.user.login,
                    "additions": pr_details.additions,
                    "deletions": pr_details.deletions,
                }
            )

    return render_template(
        "index.html",
        milestones=milestones_data,
        issues=issues_data,
        issues_count=len(issues_data),
        pull_requests=pr_data,
        pull_requests_count=len(pr_data),
    )


if __name__ == "__main__":
    logging.basicConfig(level=debug)
    app.run(host="0.0.0.0", port=5000)


# For WSGI
def create_app():
    return app
