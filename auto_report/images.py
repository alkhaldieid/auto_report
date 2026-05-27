"""Image discovery and counting."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from auto_report.config import ReportConfig, SectionConfig
from auto_report.exceptions import NoImagesFoundError


@dataclass(frozen=True)
class DepartmentImages:
    """Images discovered for one configured section."""

    section: SectionConfig
    images: tuple[Path, ...]


def natural_sort_key(path: Path) -> list[int | str]:
    """Sort image names naturally so 2.jpg comes before 10.jpg."""

    parts = re.split(r"(\d+)", path.name.lower())
    return [int(part) if part.isdigit() else part for part in parts]


def discover_department_images(
    root: Path, config: ReportConfig
) -> tuple[DepartmentImages, ...]:
    """Discover images for all configured departments."""

    discovered: list[DepartmentImages] = []
    extensions = {extension.lower() for extension in config.image_extensions}
    for section in config.sections:
        folder = root / section.folder
        images: tuple[Path, ...] = ()
        if folder.is_dir():
            images = tuple(
                sorted(
                    (
                        path
                        for path in folder.iterdir()
                        if path.is_file() and path.suffix.lower() in extensions
                    ),
                    key=natural_sort_key,
                )
            )
        discovered.append(DepartmentImages(section=section, images=images))
    return tuple(discovered)


def count_images(discovered: tuple[DepartmentImages, ...]) -> dict[str, int]:
    """Return image counts by department key."""

    return {item.section.folder: len(item.images) for item in discovered}


def require_images(discovered: tuple[DepartmentImages, ...], root: Path) -> None:
    """Raise a helpful error if the report has no images."""

    if not any(item.images for item in discovered):
        raise NoImagesFoundError(
            f"No supported images found under configured department folders in {root}."
        )
