# github-contributions

Script for reading commits (from github's API) and counting authors'
additions and deletions. You can specify repository and date interval to
check.

Configuration should be placed in python module next to `get.py` and
`nicefy.py`.

Example `config.py`:

```py
from datetime import datetime


GITHUB_ACCESS_TOKEN = "dfsdfsdfkushdfuwekjfn283ouijfouj"
GITHUB_REPOSITORY = "Ivan753/mobius"

READ_SINCE = datetime(year=2019, month=3, day=27)
READ_UNTIL = datetime(year=2019, month=4, day=10)

REPORT_FOLDER = "report"


HCTI_USER_ID = ""  # optional
HCTI_API_KEY = ""  # optional

```
