import os
import time
import threading

from datetime import datetime

from github import Github

from flask import current_app as app

from collections import defaultdict


class GitHubService:
    def __init__(self, token, repos, username_mapping):
        self.gh = Github(token)
        self.repos = repos
        self.username_mapping = username_mapping
        self.latest_data = {
            "milestones": [],
            "issues": [],
            "pull_requests": [],
            "issues_count": 0,
            "pull_requests_count": 0,
            "pending_reviews": [],
        }
        self.last_updated = None

    def fetch_data(self):
        """Main loop for updating GitHub data."""
        while True:
            self.update_general_data()
            self.update_pending_reviews()

            print("Updated github data.")
            self.last_updated = datetime.now()

            time.sleep(int(os.getenv("API_REFRESH_DURATION", 200)))

    def get_mapped_username(self, username):
        return self.username_mapping.get(username, username)

    def update_general_data(self):
        milestones_data = []
        issues_data = []
        pr_data = []

        for repo_name in self.repos:
            repo = self.gh.get_repo(repo_name)

            # Fetch milestones
            milestones = repo.get_milestones(state="open")
            for milestone in milestones:
                milestones_data.append(
                    {
                        "name": milestone.title,
                        "progress": (
                            (
                                round(
                                    milestone.closed_issues
                                    / (milestone.closed_issues + milestone.open_issues)
                                    * 100,
                                    2,
                                )
                            )
                            if (milestone.closed_issues + milestone.open_issues) > 0
                            else 0
                        ),
                        "issues": milestone.open_issues + milestone.closed_issues,
                    }
                )

            # Fetch issues
            issues = repo.get_issues(state="open")
            for issue in issues:
                if issue.pull_request:
                    continue
                issues_data.append(
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "user": issue.user.login,
                        "labels": [
                            {"name": label.name, "color": f"#{label.color}"}
                            for label in issue.labels
                        ],
                        "updated_at": issue.updated_at,
                    }
                )

            # Fetch pull requests
            pull_requests = repo.get_pulls(state="open")
            for pr in pull_requests:
                pr_data.append(
                    {
                        "number": pr.number,
                        "title": pr.title,
                        "user": pr.user.login,
                        "labels": [
                            {"name": label.name, "color": f"#{label.color}"}
                            for label in pr.labels
                        ],
                        "updated_at": pr.updated_at,
                        "is_draft": pr.draft,
                    }
                )

        self.latest_data = {
            "milestones": milestones_data,
            "issues": issues_data,
            "pull_requests": pr_data,
            "issues_count": len(issues_data),
            "pull_requests_count": len(pr_data),
        }

    def update_pending_reviews(self):
        """Fetch and update pending review requests data."""
        pending_reviews = defaultdict(list)

        for repo_name in self.repos:
            repo = self.gh.get_repo(repo_name)

            # Fetch open pull requests
            pull_requests = repo.get_pulls(state="open")
            for pr in pull_requests:
                pr_details = repo.get_pull(pr.number)

                # Check for users with pending review requests
                requested_reviewers = pr_details.get_review_requests()
                for reviewer in requested_reviewers[
                    0
                ]:  # requested_reviewers[0] contains `users`
                    mapped_name = self.get_mapped_username(reviewer.login)
                    pending_reviews[mapped_name].append(
                        {
                            "pr_number": pr.number,
                            "repo_name": repo.name,
                            "is_review": True,
                            "is_draft": pr.draft,
                        }
                    )

                # Add assignees who are not reviewers
                if pr.assignees:
                    for assignee in pr.assignees:
                        mapped_name = self.get_mapped_username(assignee.login)
                        if not any(
                            a["pr_number"] == pr.number
                            for a in pending_reviews[mapped_name]
                        ):
                            pending_reviews[mapped_name].append(
                                {
                                    "pr_number": pr.number,
                                    "repo_name": repo.name,
                                    "is_review": False,
                                    "is_draft": pr.draft,
                                }
                            )

        # Update pending reviews in the global data
        self.latest_data["pending_reviews"] = [
            {"name": name, "assignments": assignments}
            for name, assignments in pending_reviews.items()
        ]
