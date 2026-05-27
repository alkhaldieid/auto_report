"""Configuration, presets, and validation."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from auto_report.exceptions import AssetNotFoundError, ConfigurationError


@dataclass(frozen=True)
class SectionConfig:
    """A report section mapped to a folder on disk."""

    folder: str
    title: str
    caption: str | None = None


@dataclass(frozen=True)
class TitlePageConfig:
    """Title-page content and assets."""

    enabled: bool = True
    title: str = "{mode_title}"
    subtitle: str = "{period_label}"
    logo_path: str | None = None
    cover_path: str | None = None


@dataclass(frozen=True)
class ModeConfig:
    """Mode-specific report text and output behavior."""

    title: str = "Photo Report"
    subtitle: str = "{input_name}"
    output_filename: str = "{input_name}_report"
    content_section_title: str | None = None
    section_heading: str = "section"


@dataclass(frozen=True)
class ReportConfig:
    """Resolved report configuration."""

    sections: tuple[SectionConfig, ...]
    modes: dict[str, ModeConfig]
    title_page: TitlePageConfig = TitlePageConfig()
    direction: str = "ltr"
    image_extensions: tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".webp",
    )
    output_dir: str = "."
    font_name: str = "Latin Modern Roman"
    font_options: str | None = None
    contents_name: str = "Contents"
    figure_name: str = "Figure"
    image_caption_template: str = "Photos: {section_title}"


ARABIC_FACILITY_PRESET: dict[str, Any] = {
    "direction": "rtl",
    "font_name": "Amiri",
    "font_options": "Script=Arabic",
    "contents_name": "فهرس المحتويات",
    "figure_name": "الشكل",
    "image_caption_template": "صور {section_title}",
    "image_extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "output_dir": ".",
    "title_page": {
        "enabled": True,
        "title": "{mode_title}",
        "subtitle": "{mode_subtitle}",
        "logo_path": "logo.jpg",
        "cover_path": "stad.jpg",
    },
    "modes": {
        "daily": {
            "title": "التقرير اليومي لمدينة الملك عبدالعزيز الرياضية",
            "subtitle": "بتاريخ {date_ar}",
            "output_filename": "{input_name}_report",
            "section_heading": "section",
        },
        "monthly": {
            "title": "التقرير الشهري لمدينة الملك عبدالعزيز الرياضية",
            "subtitle": "{period_label}",
            "output_filename": "{input_name}_monthly_report",
            "content_section_title": "الصور الفوتوغرافية مع الوصف",
            "section_heading": "subsection",
        },
        "generic": {
            "title": "تقرير الصور لمدينة الملك عبدالعزيز الرياضية",
            "subtitle": "{input_name}",
            "output_filename": "{input_name}_report",
            "section_heading": "section",
        },
    },
    "sections": [
        {"folder": "mech", "title": "الأعمال الميكانيكية"},
        {"folder": "hvac", "title": "أعمال التكييف"},
        {"folder": "civil", "title": "الأعمال المدنية"},
        {"folder": "electric", "title": "الأعمال الكهربائية والإليكترونية"},
        {"folder": "garden", "title": "الأعمال الزراعية"},
        {"folder": "cleaning", "title": "أعمال النظافة"},
    ],
}


GENERAL_PRESET: dict[str, Any] = {
    "direction": "ltr",
    "font_name": "Latin Modern Roman",
    "font_options": None,
    "contents_name": "Contents",
    "figure_name": "Figure",
    "image_caption_template": "Photos: {section_title}",
    "image_extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "output_dir": ".",
    "title_page": {
        "enabled": True,
        "title": "{mode_title}",
        "subtitle": "{mode_subtitle}",
        "logo_path": None,
        "cover_path": None,
    },
    "modes": {
        "daily": {
            "title": "Daily Photo Report",
            "subtitle": "{date_en}",
            "output_filename": "{input_name}_report",
            "section_heading": "section",
        },
        "monthly": {
            "title": "Monthly Photo Report",
            "subtitle": "{period_label}",
            "output_filename": "{input_name}_monthly_report",
            "section_heading": "section",
        },
        "generic": {
            "title": "Photo Report",
            "subtitle": "{input_name}",
            "output_filename": "{input_name}_report",
            "section_heading": "section",
        },
    },
    "sections": [{"folder": "photos", "title": "Photos"}],
}


PRESETS: dict[str, dict[str, Any]] = {
    "arabic-facility": ARABIC_FACILITY_PRESET,
    "default": ARABIC_FACILITY_PRESET,
    "general": GENERAL_PRESET,
}

def load_config(
    path: Path | None = None,
    preset_name: str = "arabic-facility",
) -> ReportConfig:
    """Load YAML/TOML/JSON config, merged over a built-in preset."""

    preset_data = _preset_data(preset_name)
    if path is None:
        return _config_from_dict(preset_data)
    if not path.exists():
        raise ConfigurationError(f"Config file does not exist: {path}")

    user_data = _load_mapping(path)
    selected_preset = str(user_data.pop("preset", preset_name))
    merged = _deep_merge(_preset_data(selected_preset), user_data)
    return _config_from_dict(merged)


def resolve_output_dir(root: Path, config: ReportConfig, override: Path | None) -> Path:
    """Resolve and create the report output directory."""

    output_dir = override if override is not None else Path(config.output_dir)
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def resolve_asset(root: Path, asset_path: str | None, label: str) -> Path | None:
    """Resolve an optional configured asset path relative to the report root."""

    if not asset_path:
        return None
    path = Path(asset_path)
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        raise AssetNotFoundError(f"Missing {label} asset: {path}")
    return path


def _load_mapping(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")
    try:
        if suffix in {".yml", ".yaml"}:
            data = yaml.safe_load(text) or {}
        elif suffix == ".toml":
            data = _load_toml(text)
        elif suffix == ".json":
            data = json.loads(text)
        else:
            raise ConfigurationError("Config file must be .yml, .yaml, .toml, or .json.")
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ConfigurationError(f"Invalid config at {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ConfigurationError("Config file must contain a mapping/object at the top level.")
    return data


def _load_toml(text: str) -> dict[str, Any]:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigurationError(f"Invalid TOML config: {exc}") from exc


def _preset_data(name: str) -> dict[str, Any]:
    try:
        return deepcopy(PRESETS[name])
    except KeyError as exc:
        choices = ", ".join(sorted(PRESETS))
        raise ConfigurationError(
            f"Unknown preset '{name}'. Available presets: {choices}."
        ) from exc


def _config_from_dict(data: dict[str, Any]) -> ReportConfig:
    sections = _sections_from_data(data.get("sections"))
    modes = _modes_from_data(data.get("modes"))
    title_page = _title_page_from_data(data.get("title_page", {}))
    direction = str(data.get("direction", "ltr")).lower()
    if direction not in {"ltr", "rtl"}:
        raise ConfigurationError("'direction' must be either 'ltr' or 'rtl'.")

    extensions = tuple(data.get("image_extensions", GENERAL_PRESET["image_extensions"]))
    return ReportConfig(
        sections=sections,
        modes=modes,
        title_page=title_page,
        direction=direction,
        image_extensions=tuple(_normalize_extension(ext) for ext in extensions),
        output_dir=str(data.get("output_dir", ".")),
        font_name=str(data.get("font_name", "Latin Modern Roman")),
        font_options=_optional_str(data.get("font_options")),
        contents_name=str(data.get("contents_name", "Contents")),
        figure_name=str(data.get("figure_name", "Figure")),
        image_caption_template=str(
            data.get("image_caption_template", "Photos: {section_title}")
        ),
    )


def _sections_from_data(data: object) -> tuple[SectionConfig, ...]:
    if not isinstance(data, list) or not data:
        raise ConfigurationError("'sections' must be a non-empty list.")
    return tuple(_section_from_dict(item) for item in data)


def _section_from_dict(data: object) -> SectionConfig:
    if not isinstance(data, dict):
        raise ConfigurationError("Each section must be an object.")
    folder = str(data.get("folder", data.get("key", ""))).strip()
    title = str(data.get("title", data.get("arabic_name", ""))).strip()
    caption = data.get("caption")
    if not folder or not title:
        raise ConfigurationError("Each section needs 'folder' and 'title'.")
    return SectionConfig(
        folder=folder,
        title=title,
        caption=None if caption is None else str(caption),
    )


def _modes_from_data(data: object) -> dict[str, ModeConfig]:
    if not isinstance(data, dict) or not data:
        raise ConfigurationError("'modes' must define at least one mode.")
    return {str(name): _mode_from_dict(value) for name, value in data.items()}


def _mode_from_dict(data: object) -> ModeConfig:
    if not isinstance(data, dict):
        raise ConfigurationError("Each mode must be an object.")
    return ModeConfig(
        title=str(data.get("title", "Photo Report")),
        subtitle=str(data.get("subtitle", "{input_name}")),
        output_filename=str(data.get("output_filename", "{input_name}_report")),
        content_section_title=_optional_str(data.get("content_section_title")),
        section_heading=str(data.get("section_heading", "section")),
    )


def _title_page_from_data(data: object) -> TitlePageConfig:
    if not isinstance(data, dict):
        raise ConfigurationError("'title_page' must be an object.")
    return TitlePageConfig(
        enabled=bool(data.get("enabled", True)),
        title=str(data.get("title", "{mode_title}")),
        subtitle=str(data.get("subtitle", "{mode_subtitle}")),
        logo_path=_optional_str(data.get("logo_path")),
        cover_path=_optional_str(data.get("cover_path")),
    )


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_extension(extension: str) -> str:
    extension = str(extension).strip().lower()
    if not extension:
        raise ConfigurationError("Image extensions cannot be empty.")
    if not extension.startswith("."):
        extension = f".{extension}"
    return extension


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


DEFAULT_CONFIG = _config_from_dict(ARABIC_FACILITY_PRESET)
