import time
import threading
from github import Github
from flask import current_app


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
        }

    def get_mapped_username(self, username):
        return self.username_mapping.get(username, username)

    def fetch_data(self):
        while True:
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
                                    milestone.closed_issues
                                    / (milestone.closed_issues + milestone.open_issues)
                                    * 100
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
                        }
                    )

            self.latest_data = {
                "milestones": milestones_data,
                "issues": issues_data,
                "pull_requests": pr_data,
                "issues_count": len(issues_data),
                "pull_requests_count": len(pr_data),
            }

            try:
                current_app.logger.info("GitHub data updated.")
            except:
                pass
            time.sleep(60)
