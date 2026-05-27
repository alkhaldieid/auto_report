from pathlib import Path

from auto_report.config import DEFAULT_CONFIG
from auto_report.images import count_images, discover_department_images, natural_sort_key


def test_natural_sort_supports_numbered_and_arbitrary_names() -> None:
    names = [Path("10.jpg"), Path("2.jpg"), Path("before.png"), Path("1.jpg")]

    assert [path.name for path in sorted(names, key=natural_sort_key)] == [
        "1.jpg",
        "2.jpg",
        "10.jpg",
        "before.png",
    ]


def test_discover_department_images_counts_supported_files(tmp_path: Path) -> None:
    mech = tmp_path / "mech"
    mech.mkdir()
    (mech / "2.jpg").write_text("fake", encoding="utf-8")
    (mech / "10.jpg").write_text("fake", encoding="utf-8")
    (mech / "notes.txt").write_text("skip", encoding="utf-8")

    discovered = discover_department_images(tmp_path, DEFAULT_CONFIG)

    assert count_images(discovered)["mech"] == 2
    assert [path.name for path in discovered[0].images] == ["2.jpg", "10.jpg"]

