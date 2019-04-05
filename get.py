from datetime import datetime
from os import makedirs
import json

from github import Github

from config import *


# Create folder
print("Creating folder: {}/".format(REPORT_FOLDER))

makedirs(REPORT_FOLDER, exist_ok=True)

# Initialize client and get repository
print("Reading repository: {}".format(GITHUB_REPOSITORY))

repo = Github(GITHUB_ACCESS_TOKEN).get_repo(GITHUB_REPOSITORY)

FILE_CONTRIBUTIONS = REPORT_FOLDER + "/contributions.json"
FILE_CONTRIBUTIONS_COMMITS = REPORT_FOLDER + "/contributions_commits.json"

# Read or create object with infromation about contributions
try:
    with open(FILE_CONTRIBUTIONS, "r") as fh:
        contributions = json.load(fh)

except Exception:
    contributions = {}

# Read or create set with commits already counted
try:
    with open(FILE_CONTRIBUTIONS_COMMITS, "r") as fh:
        checked_commits = set(json.load(fh))

except Exception:
    checked_commits = set()


for branch in repo.get_branches():
    print("Reading branch: {}".format(branch.name))

    for commit in repo.get_commits(
        branch.name, since=READ_SINCE, until=READ_UNTIL,
    ):

        sha = commit.commit.tree.sha

        if sha in checked_commits:
            continue

        checked_commits.add(sha)

        if commit.commit.author:
            author = commit.commit.author.name
            date = commit.commit.author.date

        elif commit.commit.committer:
            author = commit.commit.committer.name
            date = commit.commit.committer.date

        else:
            continue

        # Aliases for some users
        author = {
            "Константин": "Konstantin",
            "overpoweredKLEN": "Konstantin",

            "DeuteriumQ": "Ph",
            "Metthey": "Matvey",

            "Kelayn": "Andrew Arakelyan"
        }.get(author, author)

        date = date.date().strftime("%d.%m.%Y")

        if date not in contributions:
            contributions[date] = {}

        if author not in contributions[date]:
            contributions[date][author] = [0, 0]

        contributions[date][author][0] += commit.stats.additions
        contributions[date][author][1] += commit.stats.deletions

    # Save results every cycle (for safety)
    with open(FILE_CONTRIBUTIONS, "w") as fh:
        json.dump(contributions, fh)

    with open(FILE_CONTRIBUTIONS_COMMITS, "w") as fh:
        json.dump(list(checked_commits), fh)

print(
    'Saved to "{}" and "{}"'.format(
        FILE_CONTRIBUTIONS, FILE_CONTRIBUTIONS_COMMITS
    )
)
