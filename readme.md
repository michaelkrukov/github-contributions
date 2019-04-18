# github-contributions

## Description

Scripts for reading commits (from github's API) and counting authors'
additions and deletions. You can specify repository and date interval to
check.

Configuration should be placed in python module next to `get.py` and
`nicefy.py`.

## Usage

### `get.py`

Use this script to create `contributions.json` file in `REPORT_FOLDER`.
`get.py` will also create `contributions_commits.json` file with list of
used commits' hashes.

Script will ignore:

- **Merges**. Commits with messages staring from 'merge' (case insensitive).
- **Squashed pull requests**. Commits with messages ending with
`(#digits)`, like `(#31)`.

Example `contributions.json` (numbers is `[additions, deletions]`):

```json
{
  "14.04.2019": {
    "Michael Krukov": [122, 111],
    "Matvey": [115, 24]
  },
  "15.04.2019": {
    "jagerwil": [43, 0],
    "Andrew Arakelyan": [306, 447]
  }
}
```

### `nicefy.py`

Use this script to create `report.html` file in `REPORT_FOLDER` with
contributions in table.

## Settings

Example `config.py`:

```py
from datetime import datetime


GITHUB_ACCESS_TOKEN = "dfsdfsdfkushdfuwekjfn283ouijfouj"
GITHUB_REPOSITORY = "Ivan753/mobius"

IGNORE_BRANCHES = ("master", "develop",)
IGNORE_FILES = ("package-lock.json", "Pipfile.lock",)

READ_SINCE = datetime(year=2019, month=3, day=27)
READ_UNTIL = datetime(year=2019, month=4, day=10)

REPORT_FOLDER = "report"


HCTI_USER_ID = ""  # optional
HCTI_API_KEY = ""  # optional

```
