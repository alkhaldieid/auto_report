"""LaTeX document generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from auto_report.config import ReportConfig
from auto_report.images import DepartmentImages


@dataclass(frozen=True)
class ReportContext:
    """Values needed to render a report document."""

    mode: str
    title: str
    subtitle: str
    output_filename: str
    logo_path: Path | None
    cover_path: Path | None
    config: ReportConfig
    content_section_title: str | None = None
    section_heading: str = "section"
    start_section: int = 0
    start_page: int = 1


def build_report_latex(
    context: ReportContext,
    section_images: tuple[DepartmentImages, ...],
) -> str:
    """Build a complete XeLaTeX document."""

    body = [_document_preamble(context)]
    if context.config.title_page.enabled:
        body.append(_title_page(context))
        body.append(f"\\newpage\n\\renewcommand{{\\contentsname}}{{{context.config.contents_name}}}\n")
        body.append("\\tableofcontents\n\\newpage\n")

    if context.content_section_title:
        body.append(f"\\section{{{context.content_section_title}}}\n")

    for item in section_images:
        if item.images:
            body.append(_section_block(context, item))

    body.append("\\end{document}\n")
    return "".join(body)


def _document_preamble(context: ReportContext) -> str:
    section_counter = max(context.start_section - 1, 0)
    page_counter = max(context.start_page, 1)
    direction_package = (
        "\\usepackage{arabxetex}\n" if context.config.direction == "rtl" else ""
    )
    direction_command = "\\setRL\n" if context.config.direction == "rtl" else ""
    font_options = (
        f"[{context.config.font_options}]" if context.config.font_options else ""
    )
    return rf"""
\documentclass{{article}}
\usepackage[a4paper,margin=2cm,top=2cm,bottom=3cm]{{geometry}}
\usepackage{{graphicx}}
\usepackage{{float}}
\usepackage{{fancyhdr}}
\usepackage{{fontspec}}
{direction_package}\setmainfont{font_options}{{{context.config.font_name}}}
\setlength{{\headheight}}{{30pt}}
\setlength{{\textheight}}{{650pt}}
\fancyhf{{}}
{_header_logo(context.logo_path)}
\fancyfoot[C]{{\thepage}}
\pagestyle{{fancy}}
\raggedbottom
\begin{{document}}
{direction_command}\renewcommand{{\figurename}}{{{context.config.figure_name}}}
\setcounter{{section}}{{{section_counter}}}
\setcounter{{page}}{{{page_counter}}}
"""


def _header_logo(logo_path: Path | None) -> str:
    if logo_path is None:
        return ""
    return (
        rf"\fancyhead[L]{{\includegraphics[width=0.15\textwidth]"
        rf"{{{_latex_path(logo_path)}}}}}"
    )


def _title_page(context: ReportContext) -> str:
    logo = _optional_title_image(context.logo_path, "0.85\\textwidth")
    cover = _optional_title_image(context.cover_path, "\\textwidth")
    return rf"""
\begin{{titlepage}}
    \centering
    {logo}

    \vspace{{1cm}}
    {{\Huge \textbf{{{context.title}}}}}

    \vspace{{0.5cm}}
    {{\Large {context.subtitle}}}

    \vspace{{1cm}}
    {cover}
\end{{titlepage}}
\newpage
"""


def _optional_title_image(path: Path | None, width: str) -> str:
    if path is None:
        return ""
    return rf"\includegraphics[width={width}]{{{_latex_path(path)}}}"


def _section_block(context: ReportContext, item: DepartmentImages) -> str:
    section_title = item.section.title
    output = [f"\\{context.section_heading}{{{section_title}}}\n"]
    for chunk in _chunks(item.images, 4):
        output.append("\\begin{figure}[H]\n    \\centering\n")
        output.append(_image_grid(chunk))
        output.append(
            f"    \\caption{{{_caption_for_section(context, item)}}}\n"
            "\\end{figure}\n\n"
        )
    return "".join(output)


def _caption_for_section(context: ReportContext, item: DepartmentImages) -> str:
    if item.section.caption:
        return item.section.caption
    return context.config.image_caption_template.format(
        section_title=item.section.title,
        section_folder=item.section.folder,
        mode=context.mode,
    )


def _image_grid(images: tuple[Path, ...]) -> str:
    if len(images) == 4:
        return (
            _minipage(images[0], "0.45\\textwidth")
            + "    \\hfill\n"
            + _minipage(images[1], "0.45\\textwidth")
            + "    \\vspace{0.5cm}\n\n"
            + _minipage(images[2], "0.45\\textwidth")
            + "    \\hfill\n"
            + _minipage(images[3], "0.45\\textwidth")
        )
    if len(images) == 3:
        return (
            _minipage(images[0], "0.7\\textwidth")
            + "    \\vspace{0.5cm}\n\n"
            + _minipage(images[1], "0.45\\textwidth")
            + "    \\hfill\n"
            + _minipage(images[2], "0.45\\textwidth")
        )
    if len(images) == 2:
        return (
            _minipage(images[0], "0.7\\textwidth")
            + "    \\vspace{0.5cm}\n\n"
            + _minipage(images[1], "0.7\\textwidth")
        )
    return _minipage(images[0], "0.7\\textwidth")


def _minipage(image: Path, width: str) -> str:
    return rf"""    \begin{{minipage}}{{{width}}}
        \centering
        \includegraphics[height=9cm,width=\textwidth,keepaspectratio]{{{_latex_path(image)}}}
    \end{{minipage}}
"""


def _chunks(images: tuple[Path, ...], size: int) -> tuple[tuple[Path, ...], ...]:
    return tuple(tuple(images[index : index + size]) for index in range(0, len(images), size))


def _latex_path(path: Path) -> str:
    return f"\\detokenize{{{path.as_posix()}}}"
