import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def analysis():
    df = pd.read_csv('github_issues.csv')
    date_columns = ['created_at', 'closed_at', 'updated_at']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])

    print("Issue Type Distribution:")
    print(df['type'].value_counts())

    print("\nAverage Time to Close (days):")
    print(df['time_to_close_days'].mean())

    # Plot issue creation over time
    plt.figure(figsize=(12, 6))
    df['created_at'].dt.date.value_counts().sort_index().plot()
    plt.title('Issues Created Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Issues')
    plt.show()

    # Correlation between body length and engagement
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='body_length', y='comments')
    plt.title('Relationship between Issue Length and Comments')
    plt.show()

def average_time_take_to_close_pr():
    """
    Calculate the average time taken to close pull requests.
    Returns the mean time in days.
    """
    df = pd.read_csv('github_issues.csv')
    
    # Convert date columns to datetime
    date_columns = ['created_at', 'closed_at']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])
    
    # Filter for PRs only and those that are closed
    pr_df = df[(df['type'] == 'pull_request') & (df['closed_at'].notna())]
    
    # Calculate time to close
    pr_df['time_to_close'] = (pr_df['closed_at'] - pr_df['created_at']).dt.total_seconds() / (24 * 60 * 60)
    
    return pr_df['time_to_close'].mean()

def average_time_take_to_close_issue():
    """
    Calculate the average time taken to close issues (excluding PRs).
    Returns the mean time in days.
    """
    df = pd.read_csv('github_issues.csv')
    
    # Convert date columns to datetime
    date_columns = ['created_at', 'closed_at']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])
    
    # Filter for issues only and those that are closed
    issue_df = df[(df['type'] == 'issue') & (df['closed_at'].notna())]
    
    # Calculate time to close
    issue_df['time_to_close'] = (issue_df['closed_at'] - issue_df['created_at']).dt.total_seconds() / (24 * 60 * 60)
    
    return issue_df['time_to_close'].mean()

def number_of_days_for_each_issue():
    """Create a plot showing the distribution of days taken to close issues"""
    import matplotlib.pyplot as plt
    from datetime import datetime
    df = pd.read_csv('github_issues.csv')

     # Convert date columns to datetime
    date_columns = ['created_at', 'closed_at']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])
    
    # Filter for issues only and those that are closed
    issue_df = df[(df['type'] == 'issue') & (df['closed_at'].notna())]
    issue_df['time_to_close'] = (issue_df['closed_at'] - issue_df['created_at']).dt.total_seconds() / (24 * 60 * 60)


    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.hist(issue_df["time_to_close"], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribution of Days Taken to Close Issues')
    plt.xlabel('Number of Days')
    plt.ylabel('Number of Issues')
    plt.grid(True, alpha=0.3)
    
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # # analysis()
    # # In your analysis() function, you could add:
    # print("\nAverage Time to Close PRs (days):")
    # print(average_time_take_to_close_pr())

    # print("\nAverage Time to Close Issues (days):")
    # print(average_time_take_to_close_issue())
    number_of_days_for_each_issue()