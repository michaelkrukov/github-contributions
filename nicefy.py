from itertools import chain
from datetime import datetime
import json

import requests
from requests.auth import HTTPBasicAuth


from config import *


# Templates for report
TEMPLATE = """<table><tr class="dts"><td></td>{dates}</tr>{rows}</table>"""

TEMPLATE_ROW = """<tr><td><div class="cl nm">{name}</div></td>{cols}</tr>"""

TEMPLATE_CELL = """<td><div class="cl">{}</div></td>"""

TEMPLATE_CONTRIB = \
    """<span class="ad">+{}</span><br><span class="de">-{}</span>"""

CSS = """
* {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}

html, table {
    color: #111111;
    font-family: 'Space Mono', monospace;
    background-color: #FFFFFF;
}

table {
    border-spacing: 0;
}

.nm {
    white-space: nowrap;
}

.cl {
    padding: 6px;
}

tr:nth-child(2n) {
    background-color: #DDDDDD;
}

td {
    border-right: 1px dashed #111111;
}

td:first-child {
    border-right: 1px solid #111111;
}

td:last-child {
    border-left: 1px solid #111111;
}

td:nth-last-child(1), td:nth-last-child(2) {
    border-right: 0;
}

.dts td {
    border-bottom: 1px solid #111111;
}

.ad {
    color: #007603;
}

.de {
    color: #bf0000;
}
"""


# Render report with hcti.io
def render_report_with_hcti(content):
    result = requests.post(
        "https://hcti.io/v1/image",
        auth=HTTPBasicAuth(HCTI_USER_ID, HCTI_API_KEY),
        data={
            "html": content,
            "google_fonts": "Space Mono"
        },
    )

    return result.json()["url"]


# Transform text to date
def to_date(text):
    return datetime.strptime(text, "%d.%m.%Y").date()


# Create contribution description for table
def make_contrib(data):
    return TEMPLATE_CONTRIB.format(*data)


# Create content for passed contributions data
def make_report(contributions):
    # List of used dates + "Total"
    dates = list(sorted(contributions.keys(), key=to_date)) + ["Total"]

    # List of used users
    names = sorted(list(set(
        chain(*list(day.keys() for day in contributions.values()))
    )))

    # Formatted table header
    _dates = "".join(
        TEMPLATE_CELL.format(date) for date in dates
    )

    # Create table rows
    _rows_items = []

    for name in names:
        _cols_items = []

        # Storage for "Total" column
        total = [0, 0]

        # For every user for every date create cells with user's contributions
        for date in dates:
            # Special case
            if date == "Total":
                _cols_items.append(make_contrib(total))
                continue

            # Get user contributions
            _contributions = contributions[date].get(name, [0, 0])

            # Update data for "Total" column
            total[0] += _contributions[0]
            total[1] += _contributions[1]

            _cols_items.append(make_contrib(_contributions))

        _cols = "".join(TEMPLATE_CELL.format(item) for item in _cols_items)

        _rows_items.append(
            TEMPLATE_ROW.format(
                name=name,
                cols=_cols
            )
        )

    _rows = "".join(_rows_items)

    content = TEMPLATE.format(dates=_dates, rows=_rows)

    return "<style>{styles}</style>{content}".format(
        styles=CSS,
        content=content
    )

# Load contributions data
with open(REPORT_FOLDER + "/contributions.json", "r") as fh:
    contributions = json.load(fh)

# Create report
report = make_report(contributions)

# Save report
with open(REPORT_FOLDER + "/report.html", "w") as fh:
    fh.write(report)

# Render with hcti (if uncommented)
# print(render_report_with_hcti(report))
