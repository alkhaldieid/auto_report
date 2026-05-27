"""Report orchestration and XeLaTeX compilation."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from auto_report.config import ReportConfig, resolve_asset, resolve_output_dir
from auto_report.dates import (
    format_arabic_date,
    infer_monthly_label,
    parse_daily_date_from_path,
)
from auto_report.exceptions import (
    ConfigurationError,
    FontNotFoundError,
    LatexNotFoundError,
)
from auto_report.images import discover_department_images, require_images
from auto_report.latex import ReportContext, build_report_latex


@dataclass(frozen=True)
class GeneratedReport:
    """Paths produced by a report generation run."""

    tex_path: Path
    pdf_path: Path
    compiled: bool


def generate_report(
    root: Path,
    config: ReportConfig,
    mode: str = "generic",
    output_dir: Path | None = None,
    compile_pdf: bool = True,
) -> GeneratedReport:
    """Generate a configured report for any supported mode."""

    root = root.resolve()
    _require_report_folder(root)
    context = _context(root=root, config=config, mode=mode)
    return _generate(root, config, context, output_dir, compile_pdf)


def generate_daily_report(
    root: Path,
    config: ReportConfig,
    output_dir: Path | None = None,
    compile_pdf: bool = True,
) -> GeneratedReport:
    """Generate a daily report using the configured daily mode."""

    return generate_report(
        root,
        config,
        mode="daily",
        output_dir=output_dir,
        compile_pdf=compile_pdf,
    )


def generate_monthly_report(
    root: Path,
    config: ReportConfig,
    output_dir: Path | None = None,
    compile_pdf: bool = True,
) -> GeneratedReport:
    """Generate a monthly report using the configured monthly mode."""

    return generate_report(
        root,
        config,
        mode="monthly",
        output_dir=output_dir,
        compile_pdf=compile_pdf,
    )


def _context(root: Path, config: ReportConfig, mode: str) -> ReportContext:
    try:
        mode_config = config.modes[mode]
    except KeyError as exc:
        choices = ", ".join(sorted(config.modes))
        raise ConfigurationError(
            f"Mode '{mode}' is not configured. Available modes: {choices}."
        ) from exc

    variables = _template_variables(root, mode, mode_config.title, mode_config.subtitle)
    title = _format_template(mode_config.title, variables)
    subtitle = _format_template(mode_config.subtitle, variables)
    variables = _template_variables(root, mode, title, subtitle)

    title_page_title = _format_template(config.title_page.title, variables)
    title_page_subtitle = _format_template(config.title_page.subtitle, variables)
    output_filename = _format_template(mode_config.output_filename, variables)

    logo = resolve_asset(root, config.title_page.logo_path, "logo")
    cover = resolve_asset(root, config.title_page.cover_path, "cover")
    return ReportContext(
        mode=mode,
        title=title_page_title,
        subtitle=title_page_subtitle,
        output_filename=output_filename,
        logo_path=logo,
        cover_path=cover,
        config=config,
        content_section_title=mode_config.content_section_title,
        section_heading=mode_config.section_heading,
    )


def _template_variables(
    root: Path,
    mode: str,
    mode_title: str,
    mode_subtitle: str,
) -> dict[str, str]:
    report_date = (
        parse_daily_date_from_path(root) if mode == "daily" else _optional_daily_date(root)
    )
    date_en = (
        report_date.strftime("%B %d, %Y").replace(" 0", " ")
        if report_date
        else root.name
    )
    return {
        "input_name": root.name,
        "mode": mode,
        "mode_title": mode_title,
        "mode_subtitle": mode_subtitle,
        "period_label": infer_monthly_label(root),
        "date_ar": format_arabic_date(report_date) if report_date else root.name,
        "date_en": date_en,
    }


def _optional_daily_date(root: Path) -> date | None:
    try:
        return parse_daily_date_from_path(root)
    except Exception:
        return None


def _format_template(template: str, variables: dict[str, str]) -> str:
    try:
        return template.format(**variables)
    except KeyError as exc:
        raise ConfigurationError(f"Unknown template variable: {exc}") from exc


def _generate(
    root: Path,
    config: ReportConfig,
    context: ReportContext,
    output_dir: Path | None,
    compile_pdf: bool,
) -> GeneratedReport:
    section_images = discover_department_images(root, config)
    require_images(section_images, root)
    resolved_output_dir = resolve_output_dir(root, config, output_dir)
    tex_path = resolved_output_dir / f"{context.output_filename}.tex"
    pdf_path = resolved_output_dir / f"{context.output_filename}.pdf"
    tex_path.write_text(build_report_latex(context, section_images), encoding="utf-8")

    if compile_pdf:
        validate_latex_environment(config.font_name)
        _compile_xelatex(tex_path)
    return GeneratedReport(tex_path=tex_path, pdf_path=pdf_path, compiled=compile_pdf)


def _require_report_folder(root: Path) -> None:
    if not root.is_dir():
        raise FileNotFoundError(f"Report folder does not exist: {root}")


def validate_latex_environment(font_name: str) -> None:
    """Check for XeLaTeX and, when possible, the configured font."""

    if shutil.which("xelatex") is None:
        raise LatexNotFoundError(
            "XeLaTeX was not found. Install a TeX distribution such as TeX Live, "
            "MacTeX, or MiKTeX, or rerun with --tex-only to generate LaTeX only."
        )

    fc_match = shutil.which("fc-match")
    if fc_match is not None:
        result = subprocess.run(
            [fc_match, "-f", "%{family}", font_name],
            check=False,
            capture_output=True,
            text=True,
        )
        if font_name.lower() not in result.stdout.lower():
            raise FontNotFoundError(
                f"Font '{font_name}' was not found by fontconfig. Install it or set "
                "font_name in your config file."
            )


def _compile_xelatex(tex_path: Path) -> None:
    command = ["xelatex", "-interaction=nonstopmode", tex_path.name]
    for _ in range(2):
        result = subprocess.run(
            command,
            cwd=tex_path.parent,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            log_path = tex_path.with_suffix(".log")
            raise RuntimeError(
                f"XeLaTeX failed for {tex_path}. See {log_path} for details.\n"
                f"{result.stdout[-1200:]}"
            )
