from pathlib import Path

from auto_report.cli import main


def _sample_folder(root: Path, name: str = "9-9-2030") -> Path:
    folder = root / name
    (folder / "mech").mkdir(parents=True)
    (folder / "mech" / "1.jpg").write_text("fake", encoding="utf-8")
    (folder / "logo.jpg").write_text("fake", encoding="utf-8")
    (folder / "stad.jpg").write_text("fake", encoding="utf-8")
    return folder


def test_count_command_prints_department_counts(tmp_path: Path, capsys) -> None:
    folder = _sample_folder(tmp_path)

    exit_code = main(["count", str(folder)])

    assert exit_code == 0
    assert "mech: 1" in capsys.readouterr().out


def test_daily_tex_only_writes_latex_without_xelatex(tmp_path: Path, capsys) -> None:
    folder = _sample_folder(tmp_path)

    exit_code = main(["daily", str(folder), "--tex-only"])

    assert exit_code == 0
    assert (folder / "9-9-2030_report.tex").exists()
    assert "PDF compilation skipped" in capsys.readouterr().out


def test_monthly_tex_only_writes_latex_without_xelatex(tmp_path: Path) -> None:
    folder = _sample_folder(tmp_path, name="monthly-demo")

    exit_code = main(["monthly", str(folder), "--tex-only"])

    assert exit_code == 0
    assert (folder / "monthly-demo_monthly_report.tex").exists()


def test_daily_reports_invalid_folder_date(tmp_path: Path, capsys) -> None:
    folder = _sample_folder(tmp_path, name="not-a-date")

    exit_code = main(["daily", str(folder), "--tex-only"])

    assert exit_code == 1
    assert "Expected D-M-YYYY" in capsys.readouterr().err


def test_generic_command_uses_custom_yaml_config(tmp_path: Path) -> None:
    folder = tmp_path / "inspection"
    (folder / "before").mkdir(parents=True)
    (folder / "before" / "10.jpg").write_text("fake", encoding="utf-8")
    (folder / "before" / "2.jpg").write_text("fake", encoding="utf-8")
    config_path = tmp_path / "report.yml"
    config_path.write_text(
        """
        preset: general
        title_page:
          enabled: false
        modes:
          generic:
            title: "Inspection Report"
            subtitle: "North Site"
            output_filename: "north-site"
        sections:
          - folder: before
            title: Before Photos
        """,
        encoding="utf-8",
    )

    exit_code = main(["--config", str(config_path), "generic", str(folder), "--tex-only"])

    assert exit_code == 0
    assert (folder / "north-site.tex").exists()
