#!/usr/bin/env python3

from datetime import datetime
from os import makedirs
import json
import re

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
    # Ignore branches from `IGNORE_BRANCHES` list
    if branch.name in IGNORE_BRANCHES:
        print("Skipping branch: {}".format(branch.name))
        continue

    print("Reading branch: {}".format(branch.name))

    for commit in repo.get_commits(
            branch.name, since=READ_SINCE, until=READ_UNTIL):

        message = commit.commit.message.strip().lower()

        # Ignore commits with messages starting with `merge` or
        # ending with `(#digits)` (considered to be pull request)`
        if (message.startswith("merge") or re.search(r"\(#\d+\)$", message)):
            continue

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

        additions = commit.stats.additions
        deletions = commit.stats.deletions

        # Ignore files from `IGNORE_FILES` list
        for file in commit.files:
            if file.filename in IGNORE_FILES:
                additions -= file.additions
                deletions -= file.deletions

        contributions[date][author][0] += additions
        contributions[date][author][1] += deletions

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
