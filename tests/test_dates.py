from datetime import date
from pathlib import Path

import pytest

from auto_report.dates import format_arabic_date, infer_monthly_label, parse_daily_date
from auto_report.exceptions import DateParseError


def test_parse_and_format_arabic_daily_date() -> None:
    assert parse_daily_date("9-9-2030") == date(2030, 9, 9)
    assert format_arabic_date(date(2030, 9, 9)) == "9 سبتمبر 2030"


def test_invalid_daily_date_has_clear_error() -> None:
    with pytest.raises(DateParseError, match="Expected D-M-YYYY"):
        parse_daily_date("2030-09-09")


def test_infer_monthly_label_from_folder_name() -> None:
    assert infer_monthly_label(Path("09-2030")) == "سبتمبر 2030"
    assert infer_monthly_label(Path("monthly-demo")) == "monthly-demo"

