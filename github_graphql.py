import os
from dotenv import load_dotenv
import csv
from datetime import datetime
import time
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()
TOKEN = os.getenv("gh_token")
OWNER = "python"
REPO = "cpython"

# GraphQL query for fetching issues and PRs
QUERY = """
query($owner: String!, $repo: String!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    issues(first: 100, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        id
        number
        title
        state
        createdAt
        closedAt
        updatedAt
        comments {
          totalCount
        }
        labels(first: 100) {
          nodes {
            name
          }
        }
        author {
          login
        }
        assignees(first: 10) {
          nodes {
            login
          }
        }
        milestone {
          title
        }
        body
        reactions {
          totalCount
        }
        locked
        url
      }
    }
    pullRequests(first: 100, after: $cursor, orderBy: {field: CREATED_AT, direction: DESC}) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        id
        number
        title
        state
        createdAt
        closedAt
        updatedAt
        merged
        mergedAt
        comments {
          totalCount
        }
        labels(first: 100) {
          nodes {
            name
          }
        }
        author {
          login
        }
        assignees(first: 10) {
          nodes {
            login
          }
        }
        milestone {
          title
        }
        body
        reactions {
          totalCount
        }
        locked
        url
      }
    }
  }
}
"""

def setup_client():
    transport = RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    return Client(transport=transport, fetch_schema_from_transport=True)

def fetch_data():
    client = setup_client()
    all_issues = []
    all_prs = []
    
    issues_cursor = None
    prs_cursor = None
    has_next_issues = True
    has_next_prs = True
    
    while has_next_issues or has_next_prs:
        try:
            result = client.execute(
                gql(QUERY),
                variable_values={
                    "owner": OWNER,
                    "repo": REPO,
                    "cursor": issues_cursor if has_next_issues else prs_cursor
                }
            )
            
            repo_data = result["repository"]
            
            if has_next_issues:
                issues_data = repo_data["issues"]
                all_issues.extend(issues_data["nodes"])
                has_next_issues = issues_data["pageInfo"]["hasNextPage"]
                issues_cursor = issues_data["pageInfo"]["endCursor"]
                print(f"Fetched {len(all_issues)} issues")
            
            if has_next_prs:
                prs_data = repo_data["pullRequests"]
                all_prs.extend(prs_data["nodes"])
                has_next_prs = prs_data["pageInfo"]["hasNextPage"]
                prs_cursor = prs_data["pageInfo"]["endCursor"]
                print(f"Fetched {len(all_prs)} pull requests")
            
            time.sleep(0.5)  # Be nice to GitHub's API
            
        except Exception as e:
            print(f"Error occurred: {e}")
            time.sleep(60)  # Wait if we hit rate limits
    
    return all_issues, all_prs

def process_item(item, item_type):
    labels = [label["name"] for label in item.get("labels", {}).get("nodes", [])]
    assignees = [assignee["login"] for assignee in item.get("assignees", {}).get("nodes", [])]
    
    # Calculate time to close if applicable
    created_at = item.get("createdAt")
    closed_at = item.get("closedAt")
    time_to_close = None
    if created_at and closed_at:
        created_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
        closed_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
        time_to_close = (closed_dt - created_dt).days

    return [
        item.get("id"),
        item.get("number"),
        item.get("title", "").replace("\n", " ").replace(",", " "),
        item.get("state"),
        "merged" if item.get("merged") else None if item_type == "issue" else "open",
        created_at,
        closed_at,
        item.get("updatedAt"),
        item.get("comments", {}).get("totalCount", 0),
        ",".join(labels),
        item_type,
        item.get("author", {}).get("login") if item.get("author") else None,
        ",".join(assignees),
        item.get("milestone", {}).get("title") if item.get("milestone") else None,
        len(item.get("body", "")) if item.get("body") else 0,
        item.get("reactions", {}).get("totalCount", 0),
        time_to_close,
        0,  # linked PRs (would need additional query)
        item.get("locked", False),
        item.get("comments", {}).get("totalCount", 0),
        item.get("url"),
    ]

def main():
    issues, prs = fetch_data()
    
    with open("github_issues.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "number", "title", "state", "pr_status",
            "created_at", "closed_at", "updated_at", "comments",
            "labels", "type", "author", "assignees", "milestone",
            "body_length", "reactions", "time_to_close_days",
            "linked_prs", "is_locked", "participants_count", "url"
        ])
        
        # Write issues
        for issue in issues:
            writer.writerow(process_item(issue, "issue"))
            
        # Write PRs
        for pr in prs:
            writer.writerow(process_item(pr, "pull_request"))

if __name__ == "__main__":
    main()