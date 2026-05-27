# Auto Report

General-purpose photo report generation: turn image folders into professional PDF reports with Python, YAML/TOML configuration, and XeLaTeX.

## Why This Project Matters

Many operational reports start as folders of field photos. Auto Report turns those folders into repeatable PDF reports without manually copying images into a document template. It supports both left-to-right and right-to-left reports, configurable sections, custom title pages, and natural image sorting.

The built-in `arabic-facility` preset preserves the original Arabic facility-management workflow for daily and monthly reports from department folders. That realistic preset demonstrates Arabic localization, right-to-left typesetting, and practical reporting automation while the core tool remains reusable for other organizations.

## Features

- Daily, monthly, and generic report modes
- YAML, TOML, or JSON configuration
- Built-in `arabic-facility` preset matching the sample project
- Built-in `general` preset for custom LTR reports
- Custom report title, subtitle, logo, cover image, and output filename
- LTR and RTL reports with configurable font, contents label, and figure label
- Arabic or English section names
- Custom section folder names
- Natural sorting for arbitrary image filenames, so `2.jpg` appears before `10.jpg`
- Optional section captions in config; otherwise a caption template is used
- CLI with helpful errors and no automatic PDF viewer launch
- Unit tests, Ruff linting, and GitHub Actions CI

## Quickstart

```bash
git clone https://github.com/alkhaldieid/auto_report.git
cd auto_report
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Generate LaTeX for the original Arabic sample:

```bash
auto-report daily ./sample/9-9-2030 --tex-only
```

Generate a PDF when XeLaTeX and the configured font are installed:

```bash
auto-report daily ./sample/9-9-2030
```

## CLI Examples

```bash
auto-report daily ./sample/9-9-2030
auto-report monthly ./sample/monthly-demo
auto-report generic ./sample/monthly-demo --tex-only
auto-report count ./sample/9-9-2030
auto-report --config docs/report.yml generic ./sample/custom-site --tex-only
auto-report --preset general generic ./sample/custom-site --tex-only
```

The CLI prints the generated `.tex` and `.pdf` paths instead of opening an external PDF viewer.

## Configuration

Use `report.yml` when an organization needs different sections, language, assets, or output names:

```yaml
preset: general
direction: ltr
font_name: "Latin Modern Roman"
font_options:
output_dir: reports

title_page:
  enabled: true
  title: "{mode_title}"
  subtitle: "{mode_subtitle}"
  logo_path: assets/logo.png
  cover_path: assets/cover.jpg

modes:
  generic:
    title: "Project Photo Report"
    subtitle: "North Site Inspection"
    output_filename: "north-site-photo-report"

sections:
  - folder: before
    title: Before Photos
  - folder: after
    title: After Photos
  - folder: issues
    title: Open Issues
```

Run it with:

```bash
auto-report --config report.yml generic ./path/to/report-folder --tex-only
```

Full examples:

- [docs/report.yml](docs/report.yml) for a general LTR report
- [docs/arabic-facility-report.yml](docs/arabic-facility-report.yml) for the Arabic facility-management preset
- [docs/configuration.md](docs/configuration.md) for field descriptions

## Sample Folder Structure

Arabic facility-management sample:

```text
sample/9-9-2030/
  logo.jpg
  stad.jpg
  mech/
  hvac/
  civil/
  electric/
  garden/
  cleaning/
```

General custom report example:

```text
custom-site/
  assets/
    logo.png
    cover.jpg
  before/
    2.jpg
    10.jpg
  after/
    final-check.jpg
  issues/
    cracked-tile.jpg
```

Daily mode expects the input folder name to be a date such as `9-9-2030`. Monthly and generic modes can use any folder name unless your config templates require otherwise.

## Architecture

```text
auto_report/
  cli.py        command-line interface
  config.py     presets, YAML/TOML/JSON loading, validation
  dates.py      Arabic dates and folder-name parsing
  images.py     image discovery, natural sorting, counting
  latex.py      XeLaTeX document generation
  renderer.py   orchestration and optional XeLaTeX compilation
```

The core renderer consumes resolved configuration and discovered images. Report titles, subtitles, section names, assets, direction, and output names live in presets or config files rather than in the core generation logic.

## Preview

A small generated sample PDF is included at `sample/9-9-2030/9-9-2030_report.pdf` so reviewers can inspect the original Arabic report style without installing LaTeX first.

## XeLaTeX and Font Setup

Install a TeX distribution with XeLaTeX:

- macOS: install MacTeX from <https://www.tug.org/mactex/>
- Linux: install TeX Live, for example `sudo apt install texlive-xetex texlive-lang-arabic`
- Windows: install MiKTeX from <https://miktex.org/> or TeX Live from <https://www.tug.org/texlive/>

For the Arabic preset, install Amiri:

- macOS: `brew install --cask font-amiri`
- Linux: `sudo apt install fonts-hosny-amiri`
- Windows: download Amiri from <https://www.amirifont.org/>

If LaTeX or a configured font is not available, use `--tex-only` to verify report generation without compiling the PDF.

## Testing

```bash
ruff check .
pytest
```

The tests use lightweight text fixtures with image-like extensions, so CI does not need large binary files or a TeX installation.

## GitHub Topics

Recommended repository topics: `python`, `automation`, `latex`, `arabic`, `pdf-generation`, `reporting`, `cli`.

## Roadmap

- Add per-image captions from optional sidecar metadata
- Add PDF preview screenshots in `docs/`
- Support alternate LaTeX templates for organization-specific layouts
- Add a dry-run validation command for assets, sections, and image counts

## Author

Eid Alkhaldi, PhD.

## License

MIT. See `LICENSE`.
