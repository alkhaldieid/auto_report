from pathlib import Path

from auto_report.config import DEFAULT_CONFIG
from auto_report.images import DepartmentImages
from auto_report.latex import ReportContext, build_report_latex


def test_latex_contains_arabic_sections_and_detokenized_paths(tmp_path: Path) -> None:
    image = tmp_path / "mech" / "inspection 2.jpg"
    image.parent.mkdir()
    image.write_text("fake", encoding="utf-8")
    logo = tmp_path / "logo.jpg"
    cover = tmp_path / "stad.jpg"
    logo.write_text("fake", encoding="utf-8")
    cover.write_text("fake", encoding="utf-8")
    context = ReportContext(
        mode="daily",
        title="التقرير اليومي",
        subtitle="بتاريخ 9 سبتمبر 2030",
        output_filename="daily",
        logo_path=logo,
        cover_path=cover,
        config=DEFAULT_CONFIG,
    )

    latex = build_report_latex(
        context,
        (DepartmentImages(DEFAULT_CONFIG.sections[0], (image,)),),
    )

    assert "\\setRL" in latex
    assert "الأعمال الميكانيكية" in latex
    assert "\\detokenize{" in latex
    assert "inspection 2.jpg" in latex
