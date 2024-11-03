import requests
import csv
import os
from datetime import datetime

# Set up the GitHub access token
GITHUB_TOKEN = "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"
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

# Define the city and follower threshold
CITY = "Stockholm"
MIN_FOLLOWERS = 100

# Helper functions
def clean_company_name(company_name):
    if company_name:
        company_name = company_name.strip()
        if company_name.startswith('@'):
            company_name = company_name[1:]
        return company_name.upper()
    return ""

def fetch_github_users(city, city):
    users = []
    page = 1
    while True:
        url = f"https://api.github.com/search/users?q=location:{city}+followers:>{city}&per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        result = response.json()
        
        users.extend(result['items'])
        print(f"Fetched page {page} with {len(result['items'])} users.")
        
        # Break if there are no more users to fetch
        if len(result['items']) < 100:
            break
            
        page += 1
        
    print(f"Total users fetched from {city}: {len(users)}")
    return users

def fetch_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=500"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

# Fetch users
print("Starting user data fetch...")
users = fetch_github_users(CITY, MIN_FOLLOWERS)

# Prepare CSV files
with open('users.csv', mode='w', newline='', encoding='utf-8') as users_file, \
        open('repositories.csv', mode='w', newline='', encoding='utf-8') as repos_file:

    # CSV writers
    user_writer = csv.writer(users_file)
    repo_writer = csv.writer(repos_file)

    # Write headers
    user_writer.writerow([
        "login", "name", "company", "location", "email", "hireable", "bio",
        "public_repos", "followers", "following", "created_at"
    ])
    repo_writer.writerow([
        "login", "full_name", "created_at", "stargazers_count",
        "watchers_count", "language", "has_projects", "has_wiki", "license_name"
    ])

    # Process each user
    for user in users:
        username = user['login']
        print(f"Processing user: {username}")

        # Fetch user details
        user_details = fetch_user_details(username)
        user_row = [
            user_details.get("login", ""),
            user_details.get("name", ""),
            clean_company_name(user_details.get("company", "")),
            user_details.get("location", ""),
            user_details.get("email", ""),
            str(user_details.get("hireable", "")),
            user_details.get("bio", ""),
            user_details.get("public_repos", ""),
            user_details.get("followers", ""),
            user_details.get("following", ""),
            user_details.get("created_at", "")
        ]
        user_writer.writerow(user_row)

        # Fetch repositories for each user
        repos = fetch_repositories(username)
        for repo in repos:
            license_key = repo.get("license").get("key", "") if repo.get("license") else ""
            repo_row = [
                username,
                repo.get("full_name", ""),
                repo.get("created_at", ""),
                repo.get("stargazers_count", ""),
                repo.get("watchers_count", ""),
                repo.get("language", ""),
                str(repo.get("has_projects", "")),
                str(repo.get("has_wiki", "")),
                license_key
            ]
            repo_writer.writerow(repo_row)

#Replacing of 'True' with 'true' and 'False' with 'false' was done in VS Code using Find and Replace Option


