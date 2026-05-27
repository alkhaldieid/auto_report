"""Date parsing and Arabic date formatting."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from auto_report.exceptions import DateParseError

ARABIC_MONTHS = {
    1: "يناير",
    2: "فبراير",
    3: "مارس",
    4: "أبريل",
    5: "مايو",
    6: "يونيو",
    7: "يوليو",
    8: "أغسطس",
    9: "سبتمبر",
    10: "أكتوبر",
    11: "نوفمبر",
    12: "ديسمبر",
}


def parse_daily_date(value: str) -> date:
    """Parse D-M-YYYY or DD-MM-YYYY into a date."""

    match = re.fullmatch(r"(\d{1,2})-(\d{1,2})-(\d{4})", value.strip())
    if not match:
        raise DateParseError(
            f"Invalid daily report date '{value}'. Expected D-M-YYYY, e.g. 9-9-2030."
        )
    day, month, year = (int(part) for part in match.groups())
    try:
        return date(year, month, day)
    except ValueError as exc:
        raise DateParseError(f"Invalid daily report date '{value}': {exc}") from exc


def parse_daily_date_from_path(path: Path) -> date:
    """Use the input folder name as the default daily report date."""

    return parse_daily_date(path.name)


def format_arabic_date(value: date) -> str:
    """Format a date in Arabic using Arabic month names."""

    month_name = ARABIC_MONTHS[value.month]
    return f"{value.day} {month_name} {value.year}"


def infer_monthly_label(path: Path) -> str:
    """Return a readable Arabic period label for monthly reports."""

    name = path.name.strip()
    match = re.fullmatch(r"(\d{1,2})-(\d{4})", name)
    if match:
        month, year = (int(part) for part in match.groups())
        if 1 <= month <= 12:
            return f"{ARABIC_MONTHS[month]} {year}"

    match = re.fullmatch(r"(\d{4})-(\d{1,2})", name)
    if match:
        year, month = (int(part) for part in match.groups())
        if 1 <= month <= 12:
            return f"{ARABIC_MONTHS[month]} {year}"

    return name

