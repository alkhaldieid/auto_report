from pathlib import Path

import pytest

from auto_report.config import load_config, resolve_asset
from auto_report.exceptions import AssetNotFoundError, ConfigurationError


def test_load_config_normalizes_extensions(tmp_path: Path) -> None:
    config_path = tmp_path / "report.yml"
    config_path.write_text(
        """
        preset: general
        sections:
          - folder: ops
            title: Operations
        image_extensions: [jpg, .PNG]
        title_page:
          logo_path: brand/logo.jpg
        """,
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.sections[0].folder == "ops"
    assert config.image_extensions == (".jpg", ".png")
    assert config.title_page.logo_path == "brand/logo.jpg"


def test_load_config_rejects_empty_sections(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text('{"sections": []}', encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_config(config_path)


def test_resolve_asset_reports_missing_file(tmp_path: Path) -> None:
    with pytest.raises(AssetNotFoundError, match="Missing logo asset"):
        resolve_asset(tmp_path, "logo.jpg", "logo")


def test_load_config_supports_toml_and_ltr_sections(tmp_path: Path) -> None:
    config_path = tmp_path / "report.toml"
    config_path.write_text(
        """
        preset = "general"
        direction = "ltr"

        [[sections]]
        folder = "site"
        title = "Site Photos"
        """,
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.direction == "ltr"
    assert config.sections[0].title == "Site Photos"
