# Contributing

Thank you for considering an improvement to Auto Report.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Checks

Run these before opening a pull request:

```bash
ruff check .
pytest
```

If your change affects PDF output, also generate a LaTeX file from the sample folder:

```bash
auto-report daily ./sample/9-9-2030 --tex-only
```

Use `auto-report daily ./sample/9-9-2030` when XeLaTeX and the Amiri font are installed.

## Pull Request Notes

- Keep configuration changes documented in `README.md`.
- Avoid committing LaTeX build files, local virtual environments, or generated report PDFs unless the file is an intentional demo artifact.
- Prefer small, readable changes over broad rewrites.

