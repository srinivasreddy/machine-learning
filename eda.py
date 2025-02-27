import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("gh_token")
OWNER = "python"
REPO = "cpython"

LIMIT = 1000


def fetch_issues(owner, repo, state="all", per_page=500):
    issues_data = []
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {"state": state, "per_page": per_page, "page": 1}
    headers = {"Authorization": f"token {TOKEN}"}
    counter = 0
    while counter <= LIMIT:
        print(f"the counter is {counter}")
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error:", response.json())
            break

        issues_page = response.json()
        if not issues_page:
            break
        for item in issues_page:
            if "pull_request" in item:
                pr_url = item["pull_request"]["url"]
                pr_response = requests.get(pr_url, headers=headers)
                if pr_response.status_code == 200:
                    pr_data = pr_response.json()
                    item["pr_merged"] = pr_data.get("merged", False)
                    item["pr_merged_at"] = pr_data.get("merged_at")

        issues_data.extend(issues_page)
        params["page"] += 1
        counter += 500
    return issues_data


def get_reactions(data):
    try:
        return sum(int(i) for i in data.get("reactions", {}).values())
    except ValueError:
        for i in data.get("reactions", {}).values():
            print(i, "\n")
    return 0


def main():
    issues = fetch_issues(OWNER, REPO)
    with open("github_issues.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "id",
                "number",
                "title",
                "state",
                "pr_status",
                "created_at",
                "closed_at",
                "updated_at",
                "comments",
                "labels",
                "type",
                "author",
                "assignees",
                "milestone",
                "body_length",
                "reactions",
                "time_to_close_days",
                "linked_prs",
                "is_locked",
                "participants_count",
                "url",
            ]
        )

        for issue in issues:
            if "pull_request" in issue:
                _type = "pull_request"
                if issue.get("pr_merged", False):
                    pr_status = "merged"
                elif issue["state"] == "closed":
                    pr_status = "rejected"
                else:
                    pr_status = "open"
            else:
                _type = "issue"
                pr_status = None

            labels = [label["name"] for label in issue.get("labels", [])]
            assignees = [assignee["login"] for assignee in issue.get("assignees", [])]

            # Calculate time to close if applicable
            created_at = issue.get("created_at")
            closed_at = issue.get("closed_at")
            time_to_close = None
            if created_at and closed_at:
                from datetime import datetime

                created_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                closed_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
                time_to_close = (closed_dt - created_dt).days

            writer.writerow(
                [
                    issue.get("id"),
                    issue.get("number"),
                    issue.get("title", "").replace("\n", " ").replace(",", " "),
                    issue.get("state"),
                    pr_status,
                    created_at,
                    closed_at,
                    issue.get("updated_at"),
                    issue.get("comments"),
                    ",".join(labels),
                    _type,
                    issue.get("user", {}).get("login"),
                    ",".join(assignees),
                    issue.get("milestone", {}).get("title")
                    if issue.get("milestone")
                    else None,
                    len(issue.get("body", "")) if issue.get("body") else 0,
                    get_reactions(issue) if issue.get("reactions") else 0,
                    time_to_close,
                    len(issue.get("pull_request", {}).get("links", []))
                    if "pull_request" in issue
                    else 0,
                    issue.get("locked", False),
                    issue.get(
                        "comments", 0
                    ),  # Using comments as a proxy for participants
                    issue.get("html_url"),
                ]
            )


if __name__ == "__main__":
    main()
