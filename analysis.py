import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def analysis():
    df = pd.read_csv("github_issues.csv")
    date_columns = ["created_at", "closed_at", "updated_at"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    print("Issue Type Distribution:")
    print(df["type"].value_counts())

    print("\nAverage Time to Close (days):")
    print(df["time_to_close_days"].mean())

    # Plot issue creation over time
    plt.figure(figsize=(12, 6))
    df["created_at"].dt.date.value_counts().sort_index().plot()
    plt.title("Issues Created Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Issues")
    plt.show()

    # Correlation between body length and engagement
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="body_length", y="comments")
    plt.title("Relationship between Issue Length and Comments")
    plt.show()


def average_time_take_to_close_pr():
    """
    Calculate the average time taken to close pull requests.
    Returns the mean time in days.
    """
    df = pd.read_csv("github_issues.csv")

    # Convert date columns to datetime
    date_columns = ["created_at", "closed_at"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    # Filter for PRs only and those that are closed
    pr_df = df[(df["type"] == "pull_request") & (df["closed_at"].notna())]

    # Calculate time to close
    pr_df["time_to_close"] = (
        pr_df["closed_at"] - pr_df["created_at"]
    ).dt.total_seconds() / (24 * 60 * 60)

    return pr_df["time_to_close"].mean()


def average_time_take_to_close_issue():
    """
    Calculate the average time taken to close issues (excluding PRs).
    Returns the mean time in days.
    """
    df = pd.read_csv("github_issues.csv")

    # Convert date columns to datetime
    date_columns = ["created_at", "closed_at"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    # Filter for issues only and those that are closed
    issue_df = df[(df["type"] == "issue") & (df["closed_at"].notna())]

    # Calculate time to close
    issue_df["time_to_close"] = (
        issue_df["closed_at"] - issue_df["created_at"]
    ).dt.total_seconds() / (24 * 60 * 60)

    return issue_df["time_to_close"].mean()


def number_of_days_for_each_issue():
    """Create a plot showing the distribution of days taken to close issues"""
    import matplotlib.pyplot as plt
    from datetime import datetime

    df = pd.read_csv("github_issues.csv")

    # Convert date columns to datetime
    date_columns = ["created_at", "closed_at"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    # Filter for issues only and those that are closed
    issue_df = df[(df["type"] == "issue") & (df["closed_at"].notna())]
    issue_df["time_to_close"] = (
        issue_df["closed_at"] - issue_df["created_at"]
    ).dt.total_seconds() / (24 * 60 * 60)

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.hist(issue_df["time_to_close"], bins=30, color="skyblue", edgecolor="black")
    plt.title("Distribution of Days Taken to Close Issues")
    plt.xlabel("Number of Days")
    plt.ylabel("Number of Issues")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def most_active_issue_creators(top_n=10):
    """
    Find users who opened the most issues.
    Args:
        top_n: Number of top users to return (default: 10)
    """
    df = pd.read_csv("github_issues.csv")
    
    # Filter for issues only
    issues_df = df[df["type"] == "issue"]
    
    # Count issues by user
    issue_counts = issues_df["user"].value_counts()
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    issue_counts.head(top_n).plot(kind='bar')
    plt.title(f"Top {top_n} Users by Number of Issues Opened")
    plt.xlabel("Username")
    plt.ylabel("Number of Issues")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    return issue_counts.head(top_n)


def most_active_pr_authors(top_n=10):
    """
    Find users with the most merged pull requests.
    Args:
        top_n: Number of top users to return (default: 10)
    """
    df = pd.read_csv("github_issues.csv")
    
    # Filter for merged PRs only
    merged_prs_df = df[(df["type"] == "pull_request") & (df["state"] == "closed")]
    
    # Count PRs by user
    pr_counts = merged_prs_df["user"].value_counts()
    
    # Create visualization
    plt.figure(figsize=(12, 6))
    pr_counts.head(top_n).plot(kind='bar')
    plt.title(f"Top {top_n} Users by Number of Merged PRs")
    plt.xlabel("Username")
    plt.ylabel("Number of Pull Requests")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    return pr_counts.head(top_n)


def analyze_issue_labels(top_n=10):
    """Analyze the most common issue labels and their distribution"""
    df = pd.read_csv("github_issues.csv")
    
    # Assuming labels are stored as a string list, might need preprocessing
    label_counts = df["labels"].value_counts()
    
    plt.figure(figsize=(12, 6))
    label_counts.head(top_n).plot(kind='bar')
    plt.title(f"Top {top_n} Most Common Issue Labels")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    return label_counts.head(top_n)


def analyze_first_response_time():
    """Analyze how long it takes to get the first response on issues"""
    df = pd.read_csv("github_issues.csv")
    
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["first_response_at"] = pd.to_datetime(df["first_response_at"])
    
    df["response_time_days"] = (
        df["first_response_at"] - df["created_at"]
    ).dt.total_seconds() / (24 * 60 * 60)
    
    plt.figure(figsize=(12, 6))
    plt.hist(df["response_time_days"].dropna(), bins=50)
    plt.title("Distribution of Time to First Response")
    plt.xlabel("Days")
    plt.ylabel("Number of Issues")
    plt.show()


def analyze_issue_patterns():
    """Analyze when issues are typically created and resolved"""
    df = pd.read_csv("github_issues.csv")
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # Issues by day of week
    plt.figure(figsize=(12, 6))
    df["created_at"].dt.day_name().value_counts().plot(kind='bar')
    plt.title("Issues Created by Day of Week")
    plt.xlabel("Day")
    plt.ylabel("Number of Issues")
    plt.tight_layout()
    plt.show()
    
    # Issues by month
    plt.figure(figsize=(12, 6))
    df["created_at"].dt.month_name().value_counts().plot(kind='bar')
    plt.title("Issues Created by Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Issues")
    plt.tight_layout()
    plt.show()


def analyze_issue_complexity():
    """Analyze issue complexity based on body length, comments, and time to close"""
    df = pd.read_csv("github_issues.csv")
    
    plt.figure(figsize=(15, 5))
    
    # Create a subplot with 3 graphs
    plt.subplot(131)
    sns.boxplot(x="type", y="body_length", data=df)
    plt.title("Body Length by Type")
    
    plt.subplot(132)
    sns.boxplot(x="type", y="comments", data=df)
    plt.title("Comments by Type")
    
    plt.subplot(133)
    sns.boxplot(x="type", y="time_to_close_days", data=df)
    plt.title("Time to Close by Type")
    
    plt.tight_layout()
    plt.show()


def analyze_user_engagement():
    """Analyze how user engagement has changed over time"""
    df = pd.read_csv("github_issues.csv")
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # Group by month and count unique users
    monthly_users = df.groupby(df["created_at"].dt.to_period("M"))["user"].nunique()
    
    plt.figure(figsize=(12, 6))
    monthly_users.plot(kind='line', marker='o')
    plt.title("Unique Users per Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Unique Users")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def analyze_contributor_retention():
    """
    Analyze how many contributors stay active over time and identify repeat contributors
    """
    df = pd.read_csv("github_issues.csv")
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # Add month-year field for grouping
    df["month_year"] = df["created_at"].dt.to_period("M")
    
    # Get first contribution date for each user
    first_contributions = df.groupby("user")["created_at"].min()
    
    # Calculate contributor retention by months since first contribution
    retention_data = []
    for user, first_date in first_contributions.items():
        user_activity = df[df["user"] == user]["month_year"].unique()
        months_active = len(user_activity)
        retention_data.append(months_active)
    
    plt.figure(figsize=(10, 6))
    plt.hist(retention_data, bins=20)
    plt.title("Distribution of Contributor Activity Duration")
    plt.xlabel("Number of Months Active")
    plt.ylabel("Number of Contributors")
    plt.show()


def analyze_collaboration_patterns():
    """
    Analyze how users interact with each other through comments and reactions
    """
    df = pd.read_csv("github_issues.csv")
    
    # Analyze issues with most community engagement
    engagement_score = df["comments"] + df["reactions"]
    top_engaged = df.nlargest(10, engagement_score)
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(top_engaged)), engagement_score[top_engaged.index])
    plt.title("Most Engaging Issues/PRs")
    plt.xlabel("Issue Number")
    plt.ylabel("Total Engagement (Comments + Reactions)")
    plt.xticks(range(len(top_engaged)), top_engaged["number"], rotation=45)
    plt.tight_layout()
    plt.show()


def analyze_newcomer_experience():
    """
    Analyze the experience of new contributors and their first interactions
    """
    df = pd.read_csv("github_issues.csv")
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # For each user, get their first contribution
    first_contributions = df.sort_values("created_at").groupby("user").first()
    
    # Analyze response times for first-time contributors
    first_contributions["response_time"] = pd.to_datetime(first_contributions["first_response_at"]) - \
                                         pd.to_datetime(first_contributions["created_at"])
    first_contributions["response_days"] = first_contributions["response_time"].dt.total_seconds() / (24 * 60 * 60)
    
    plt.figure(figsize=(10, 6))
    plt.hist(first_contributions["response_days"].dropna(), bins=30)
    plt.title("Response Time for First-time Contributors")
    plt.xlabel("Days to First Response")
    plt.ylabel("Number of Contributors")
    plt.show()


def analyze_community_growth():
    """
    Analyze the growth of the community over time
    """
    df = pd.read_csv("github_issues.csv")
    df["created_at"] = pd.to_datetime(df["created_at"])
    
    # Monthly new contributors
    monthly_new_contributors = df.groupby(df["created_at"].dt.to_period("M"))["user"].nunique().cumsum()
    
    plt.figure(figsize=(12, 6))
    monthly_new_contributors.plot(kind='line', marker='o')
    plt.title("Cumulative Growth of Community Members")
    plt.xlabel("Month")
    plt.ylabel("Total Number of Contributors")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def analyze_contribution_diversity():
    """
    Analyze the diversity of contribution types and participation patterns
    """
    df = pd.read_csv("github_issues.csv")
    
    # Calculate contribution type distribution per user
    user_contribution_types = df.groupby("user")["type"].value_counts().unstack().fillna(0)
    
    # Calculate ratio of PRs to Issues for active users
    user_contribution_types["pr_to_issue_ratio"] = user_contribution_types["pull_request"] / \
                                                  user_contribution_types["issue"].replace(0, 1)
    
    plt.figure(figsize=(12, 6))
    plt.hist(user_contribution_types["pr_to_issue_ratio"], bins=30)
    plt.title("Distribution of PR to Issue Ratio per User")
    plt.xlabel("PR to Issue Ratio")
    plt.ylabel("Number of Users")
    plt.show()


if __name__ == "__main__":
    # # analysis()
    # # In your analysis() function, you could add:
    # print("\nAverage Time to Close PRs (days):")
    # print(average_time_take_to_close_pr())

    # print("\nAverage Time to Close Issues (days):")
    # print(average_time_take_to_close_issue())
    number_of_days_for_each_issue()

    print("\nTop Issue Creators:")
    print(most_active_issue_creators())
    
    print("\nTop PR Authors:")
    print(most_active_pr_authors())