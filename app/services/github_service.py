import time
import threading

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
            "branch_graph": {},
        }

    def fetch_data(self):
        """Main loop for updating GitHub data."""
        while True:
            self.update_general_data()
            self.update_pending_reviews()
            self.fetch_branch_graph()

            time.sleep(90)

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

        self.latest_data["milestones"] = milestones_data
        self.latest_data["issues"] = issues_data
        self.latest_data["pull_requests"] = pr_data
        self.latest_data["issues_count"] = len(issues_data)
        self.latest_data["pull_requests_count"] = len(pr_data)

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
                                }
                            )

        # Update pending reviews in the global data
        self.latest_data["pending_reviews"] = [
            {"name": name, "assignments": assignments}
            for name, assignments in pending_reviews.items()
        ]

    def fetch_branch_graph(self):
        """Fetch branch and commit data for branches with open PRs and the default branch."""
        branch_graph = {}

        for repo_name in self.repos:
            repo = self.gh.get_repo(repo_name)
            repo_data = {"repo_name": repo.full_name, "branches": []}

            # Include the default branch
            default_branch_name = repo.default_branch
            default_branch_commits = repo.get_commits(sha=default_branch_name)[:20]
            default_branch_info = {
                "name": default_branch_name,
                "commits": [
                    {
                        "sha": commit.sha,
                        "message": commit.commit.message,
                        "author": (
                            commit.commit.author.name
                            if commit.commit.author
                            else "Unknown"
                        ),
                        "date": (
                            commit.commit.author.date.isoformat()
                            if commit.commit.author
                            else None
                        ),
                    }
                    for commit in default_branch_commits
                ],
                "target_pr": None,  # Default branch is not targeted by a PR
            }
            repo_data["branches"].append(default_branch_info)

            # Fetch branches with open pull requests
            pull_requests = repo.get_pulls(state="open")
            for pr in pull_requests:
                branch_name = pr.head.ref
                target_branch = pr.base.ref

                # Fetch the last 20 commits for the branch
                commits = repo.get_commits(sha=branch_name)[:20]
                branch_info = {
                    "name": branch_name,
                    "commits": [
                        {
                            "sha": commit.sha,
                            "message": commit.commit.message,
                            "author": (
                                commit.commit.author.name
                                if commit.commit.author
                                else "Unknown"
                            ),
                            "date": (
                                commit.commit.author.date.isoformat()
                                if commit.commit.author
                                else None
                            ),
                        }
                        for commit in commits
                    ],
                    "target_pr": target_branch,
                }

                repo_data["branches"].append(branch_info)

            # Only include on branches that are not empty.
            if len(repo_data["branches"]) > 0:
                branch_graph[repo.full_name] = repo_data
            else:
                pass

        # Update global data structure
        self.latest_data["branch_graph"] = branch_graph
