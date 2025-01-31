import requests
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


def check_github_updates(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"

    try:
        logging.info(
            f"🔍 Checking for updates in the GitHub repository: {repo_owner}/{repo_name}"
        )
        response = requests.get(url)
        response.raise_for_status()

        commits = response.json()
        if commits:
            latest_commit = commits[0]
            commit_sha = latest_commit["sha"]
            commit_message = latest_commit["commit"]["message"]
            commit_date = datetime.strptime(
                latest_commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ"
            )

            logging.info(f"✅ Repository checked successfully!")
            logging.info(f"📅 Latest commit date: {commit_date}")
            logging.info(f"🔑 Commit SHA: {commit_sha[:7]}")
            logging.info(f"💬 Commit message: {commit_message}")

            return True, commit_sha, commit_message, commit_date
        else:
            logging.warning(
                f"⚠️ No commits found in the repository: {repo_owner}/{repo_name}"
            )
            return False, None, None, None

    except requests.exceptions.RequestException as e:
        logging.error(
            f"❌ Error occurred while checking for updates in {repo_owner}/{repo_name}: {str(e)}"
        )
        return False, None, None, None


def check_multiple_repositories(repositories):
    updated_repos = []
    for repo in repositories:
        repo_owner, repo_name = repo.split("/")
        has_updates, _, _, _ = check_github_updates(repo_owner, repo_name)
        if has_updates:
            updated_repos.append(repo)
    return updated_repos


def main(repositories):
    updated_repos = check_multiple_repositories(repositories)

    if updated_repos:
        logging.info("🎉 Updates found in the following repositories:")
        for repo in updated_repos:
            logging.info(f"  - {repo}")
    else:
        logging.info("😴 No updates found in any of the repositories.")

    return updated_repos
