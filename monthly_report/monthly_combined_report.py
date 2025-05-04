import os
import subprocess

# List of directories to count images in
directories = ["mech", "hvac", "civil", "electric", "garden", "cleaning"]

# Supported image file extensions
image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff")

# Dictionary mapping English directory names to Arabic section titles
arabic_section_names = {
    "hvac": "أعمال التكييف",
    "mech": "الأعمال الميكانيكية",
    "electric": "الأعمال الكهربائية والإليكترونية",
    "civil": "الأعمال المدنية",
    "garden": "الأعمال الزراعية",
    "cleaning": "أعمال النظافة",
}


def get_image_files(directory):
    """Return a list of all image files in the given directory."""
    return [
        file
        for file in os.listdir(directory)
        if file.lower().endswith(image_extensions)
    ]


def generate_latex_for_four_images(directory, image_files, start_index):
    """Generate LaTeX for four images in a 2x2 grid with specified height and width."""
    return f"""
    % First row
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index]}}}
    \\end{{minipage}}
    \\hfill
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index + 1]}}}
    \\end{{minipage}}
    \\vspace{{0.5cm}} % Vertical space between rows

    % Second row
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index + 2]}}}
    \\end{{minipage}}
    \\hfill
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index + 3]}}}
    \\end{{minipage}}
    """


def generate_latex_for_three_images(directory, image_files, start_index):
    """Generate LaTeX for three images: one on top and two below, with specified height and width."""
    return f"""
    % One image on top
    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index]}}}
    \\end{{minipage}}
    \\vspace{{0.5cm}} % Vertical space between rows

    % Two images below
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index + 1]}}}
    \\end{{minipage}}
    \\hfill
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index + 2]}}}
    \\end{{minipage}}
    """


def generate_latex_for_two_images(directory, image_files, start_index):
    """Generate LaTeX for two images: vertically stacked, with specified height and width."""
    return f"""
    % Two images stacked vertically
    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index]}}}
    \\end{{minipage}}
    \\vspace{{0.5cm}} % Vertical space between rows

    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index + 1]}}}
    \\end{{minipage}}
    """


def generate_latex_for_one_image(directory, image_files, start_index):
    """Generate LaTeX for one image centered with specified height and width."""
    return f"""
    % One image centered
    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{image_files[start_index]}}}
    \\end{{minipage}}
    """


def generate_latex_for_images(directory, image_files):
    """Generate LaTeX code for the images in the directory."""
    section_title = arabic_section_names.get(directory, directory)
    latex_code = f"\\subsection{{{section_title}}}\n"

    total_images = len(image_files)
    for i in range(0, total_images, 4):
        remaining_images = min(4, total_images - i)

        # Add a fixed vertical space before each figure block
        latex_code += "\\vspace*{2cm}\n"
        latex_code += "\\begin{figure}[H]\n    \\centering\n"

        if remaining_images == 4:
            latex_code += generate_latex_for_four_images(directory, image_files, i)
        elif remaining_images == 3:
            latex_code += generate_latex_for_three_images(directory, image_files, i)
        elif remaining_images == 2:
            latex_code += generate_latex_for_two_images(directory, image_files, i)
        elif remaining_images == 1:
            latex_code += generate_latex_for_one_image(directory, image_files, i)

        latex_code += f"    \\caption{{صور {section_title}}}\n\\end{{figure}}\n\n"

    return latex_code


def generate_report():
    """Generate the LaTeX code for the report portion."""
    root_directory = os.getcwd()  # Get the current working directory
    report_latex = ""

    # Start the report LaTeX structure with the main section and resetting counters
    report_latex += """
\\documentclass{article}
\\usepackage[a4paper,margin=2cm,top=2cm,bottom=3cm]{geometry}
\\usepackage{graphicx}
\\usepackage{float}
\\usepackage{fancyhdr}
\\usepackage{fontspec}
\\usepackage{afterpage}
\\usepackage{arabxetex}
\\setmainfont[Script=Arabic]{Amiri}

% Configure the header and footer
\\fancyhf{}  % Clear all header and footer fields
\\fancyhead[L]{\\includegraphics[width=0.15\\textwidth]{logo.jpg}}  % Add logo to the left in the header
\\fancyfoot[C]{\\thepage}  % Page number at the bottom center
\\setlength{\\headheight}{30pt}  % Increase space between header and text
\\setlength{\\textheight}{650pt}  % Adjust text height to prevent footer overlap

% Reset section and page numbering
\\setcounter{section}{6}  % Start section numbering from 7
\\setcounter{page}{24}  % Start page numbering from 28

% Page layout configuration
\\pagestyle{fancy}  % Apply the fancy page style globally
\\raggedbottom  % Avoid stretching the page content
\\begin{document}
\\setRL  % Right-to-left text
\\renewcommand{\\figurename}{الشكل}

% Main section for the report
\\section{الصور الفوتوغرافية مع الوصف}
"""

    # Generate subsections for each directory
    for directory in directories:
        full_path = os.path.join(root_directory, directory)
        if os.path.exists(full_path):
            image_files = get_image_files(full_path)
            if image_files:
                report_latex += generate_latex_for_images(directory, image_files)

    report_latex += "\\end{document}"
    return report_latex


if __name__ == "__main__":
    latex_code = generate_report()

    # Generate the filename in the format report.tex
    tex_filename = "report.tex"
    pdf_filename = "report.pdf"

    # Write the LaTeX code to the file
    with open(tex_filename, "w") as f:
        f.write(latex_code)

    print(f"LaTeX code generated and saved to {tex_filename}.")

    # Compile the LaTeX file twice using xelatex with nonstop mode
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename])
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename])

    # Open the resulting PDF with evince (if available)
    subprocess.run(["evince", pdf_filename])
