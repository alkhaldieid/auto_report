"""Command-line interface for auto-report."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from auto_report.config import PRESETS, load_config
from auto_report.exceptions import AutoReportError
from auto_report.images import count_images, discover_department_images
from auto_report.renderer import (
    generate_daily_report,
    generate_monthly_report,
    generate_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auto-report",
        description="Generate photo PDF reports from configured image folders.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Optional YAML, TOML, or JSON report config file.",
    )
    parser.add_argument(
        "--preset",
        default="arabic-facility",
        choices=sorted(PRESETS),
        help="Built-in preset used when no config is supplied, or as a config base.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    for command, help_text in (
        ("daily", "Generate a daily report from a D-M-YYYY folder."),
        ("monthly", "Generate a monthly report from a department image folder."),
    ):
        subparser = subparsers.add_parser(command, help=help_text)
        subparser.add_argument("folder", type=Path, help="Report input folder.")
        subparser.add_argument(
            "-o",
            "--output-dir",
            type=Path,
            help="Output directory. Defaults to the configured output directory.",
        )
        subparser.add_argument(
            "--tex-only",
            action="store_true",
            help="Only generate the .tex file; skip XeLaTeX PDF compilation.",
        )

    generic_parser = subparsers.add_parser(
        "generic",
        help="Generate a generic configured report.",
    )
    generic_parser.add_argument("folder", type=Path, help="Report input folder.")
    generic_parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Output directory. Defaults to the configured output directory.",
    )
    generic_parser.add_argument(
        "--mode",
        default="generic",
        help="Configured mode name to render. Defaults to generic.",
    )
    generic_parser.add_argument(
        "--tex-only",
        action="store_true",
        help="Only generate the .tex file; skip XeLaTeX PDF compilation.",
    )

    count_parser = subparsers.add_parser("count", help="Count images by configured section.")
    count_parser.add_argument("folder", type=Path, help="Report input folder.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config, preset_name=args.preset)
        if args.command == "daily":
            result = generate_daily_report(
                args.folder,
                config,
                output_dir=args.output_dir,
                compile_pdf=not args.tex_only,
            )
            _print_result(result.tex_path, result.pdf_path, result.compiled)
        elif args.command == "monthly":
            result = generate_monthly_report(
                args.folder,
                config,
                output_dir=args.output_dir,
                compile_pdf=not args.tex_only,
            )
            _print_result(result.tex_path, result.pdf_path, result.compiled)
        elif args.command == "generic":
            result = generate_report(
                args.folder,
                config,
                mode=args.mode,
                output_dir=args.output_dir,
                compile_pdf=not args.tex_only,
            )
            _print_result(result.tex_path, result.pdf_path, result.compiled)
        elif args.command == "count":
            if not args.folder.is_dir():
                raise FileNotFoundError(f"Report folder does not exist: {args.folder}")
            counts = count_images(discover_department_images(args.folder, config))
            for department, count in counts.items():
                print(f"{department}: {count}")
    except (AutoReportError, FileNotFoundError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


def _print_result(tex_path: Path, pdf_path: Path, compiled: bool) -> None:
    print(f"LaTeX written to: {tex_path}")
    if compiled:
        print(f"PDF written to: {pdf_path}")
    else:
        print("PDF compilation skipped (--tex-only).")


if __name__ == "__main__":
    raise SystemExit(main())
