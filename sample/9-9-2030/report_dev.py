import os
import subprocess

# List of directories to count images in
directories = ['mech', 'hvac', 'civil', 'electric', 'garden', 'cleaning']

# Supported image file extensions
image_extensions = ('.jpg', '.jpeg')

# Dictionary mapping English directory names to Arabic section titles
arabic_section_names = {
    'hvac': 'أعمال التكييف',
    'mech': 'الأعمال الميكانيكية',
    'electric': 'الأعمال الكهربائية والإليكترونية',
    'civil': 'الأعمال المدنية',
    'garden': 'الأعمال الزراعية',
    'cleaning': 'أعمال النظافة'
}

# Dictionary to map month numbers to Arabic month names
arabic_months = {
    '01': 'يناير',
    '02': 'فبراير',
    '03': 'مارس',
    '04': 'أبريل',
    '05': 'مايو',
    '06': 'يونيو',
    '07': 'يوليو',
    '08': 'أغسطس',
    '09': 'سبتمبر',
    '10': 'أكتوبر',
    '11': 'نوفمبر',
    '12': 'ديسمبر'
}

def count_images_in_directory(directory):
    """Count the number of image files in a given directory."""
    return len([file for file in os.listdir(directory) if file.lower().endswith(image_extensions)])

def generate_latex_for_images(directory, count):
    """Generate LaTeX code for the images in the directory."""
    section_title = arabic_section_names.get(directory, directory)

    latex_code = f"\\section{{{section_title}}}\n"
    
    for i in range(1, count + 1, 4):
        remaining_images = min(4, count - i + 1)
        
        latex_code += "\\begin{figure}[H]\n    \\centering\n"

        if remaining_images == 4:
            latex_code += generate_latex_for_four_images(directory, i)
        elif remaining_images == 3:
            latex_code += generate_latex_for_three_images(directory, i)
        elif remaining_images == 2:
            latex_code += generate_latex_for_two_images(directory, i)
        elif remaining_images == 1:
            latex_code += generate_latex_for_one_image(directory, i)
        
        latex_code += f"    \\caption{{صور {section_title}}}\n\\end{{figure}}\n\n"
    
    return latex_code

def find_image_file(directory, image_number):
    """Find the image file with either .jpg or .jpeg extension."""
    for ext in image_extensions:
        image_file = os.path.join(directory, f"{image_number}{ext}")
        if os.path.exists(image_file):
            return f"{image_number}{ext}"
    return None

def generate_latex_for_four_images(directory, start_index):
    """Generate LaTeX for four images in a 2x2 grid with specified height and width."""
    return f"""
    % First row
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index)}}}
    \\end{{minipage}}
    \\hfill
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index + 1)}}}
    \\end{{minipage}}
    \\vspace{{0.5cm}} % Vertical space between rows

    % Second row
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index + 2)}}}
    \\end{{minipage}}
    \\hfill
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index + 3)}}}
    \\end{{minipage}}
    """

def generate_latex_for_three_images(directory, start_index):
    """Generate LaTeX for three images: one on top and two below, with specified height and width."""
    return f"""
    % One image on top
    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index)}}}
    \\end{{minipage}}
    \\vspace{{0.5cm}} % Vertical space between rows

    % Two images below
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index + 1)}}}
    \\end{{minipage}}
    \\hfill
    \\begin{{minipage}}{{0.45\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index + 2)}}}
    \\end{{minipage}}
    """

def generate_latex_for_two_images(directory, start_index):
    """Generate LaTeX for two images: vertically stacked, with specified height and width."""
    return f"""
    % Two images stacked vertically
    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index)}}}
    \\end{{minipage}}
    \\vspace{{0.5cm}} % Vertical space between rows

    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index + 1)}}}
    \\end{{minipage}}
    """

def generate_latex_for_one_image(directory, start_index):
    """Generate LaTeX for one image centered with specified height and width."""
    return f"""
    % One image centered
    \\begin{{minipage}}{{0.7\\textwidth}}
        \\centering
        \\includegraphics[height=9cm,width=\\textwidth]{{{directory}/{find_image_file(directory, start_index)}}}
    \\end{{minipage}}
    """

def format_date_arabic(date_string):
    """Format a date string (DD-MM-YYYY) into Arabic."""
    day, month, year = date_string.split('-')
    
    # Handle one-digit days and months by padding with zero if necessary
    day = day.zfill(2)
    month = month.zfill(2)

    arabic_month = arabic_months.get(month, month)
    return f"{int(day)} {arabic_month} {year}"

def generate_report():
    """Generate the LaTeX code for the entire report, including the formatted date."""
    root_directory = os.getcwd()  # Get the current working directory
    report_latex = ""

    # Extract the date from the root directory name (assuming it's named as DD-MM-YYYY)
    date_string = os.path.basename(root_directory)
    formatted_date = format_date_arabic(date_string)

    # Start the report with the formatted date in Arabic
    report_latex += f"""
\\documentclass{{article}}
\\usepackage[a4paper,margin=2cm,top=2cm]{{geometry}}
\\usepackage{{graphicx}}
\\usepackage{{float}}
\\usepackage{{fancyhdr}}
\\usepackage{{fontspec}}
\\usepackage{{arabxetex}}
\\setmainfont[Script=Arabic]{{Amiri}}

\\begin{{document}}
\\setRL
\\renewcommand{{\\figurename}}{{الشكل}}

\\fancypagestyle{{plain}}{{%
    \\fancyhf{{}}
    \\fancyhead[L]{{\\hspace{{-2cm}}\\includegraphics[width=0.25\\textwidth]{{logo.jpg}}}}
    \\renewcommand{{\\headrulewidth}}{{0pt}}
}}
\\pagestyle{{plain}}

\\begin{{titlepage}}
    \\centering
    \\includegraphics[width=1 \\textwidth]{{logo.jpg}}

    \\vspace{{1cm}}
    {{\\Huge \\textbf{{التقرير اليومي لمدينة الملك عبدالعزيز الرياضية}}}}

    \\vspace{{0.5cm}}
    {{\\Large بتاريخ}} 
    {{\\Large {formatted_date}}}

    \\vspace{{1cm}}
    \\includegraphics[width=\\textwidth]{{stad.jpg}}
\\end{{titlepage}}
\\newpage
\\renewcommand{{\\contentsname}}{{فهرس المحتويات}}
\\newpage
\\tableofcontents
\\newpage
"""

    # Generate sections for each directory
    for directory in directories:
        full_path = os.path.join(root_directory, directory)
        if os.path.exists(full_path):
            image_count = count_images_in_directory(full_path)
            if image_count > 0:
                report_latex += generate_latex_for_images(directory, image_count)
    
    report_latex += "\\end{document}"
    return report_latex


if __name__ == "__main__":
    latex_code = generate_report()

    # Extract the date from the root directory name (assuming it's named as DD-MM-YYYY)
    root_directory = os.getcwd()
    date_string = os.path.basename(root_directory)

    # Generate the filename in the format DD-MM-YYYY_report.tex
    tex_filename = f"{date_string}_report.tex"
    pdf_filename = f"{date_string}_report.pdf"

    # Write the LaTeX code to the file
    with open(tex_filename, "w") as f:
        f.write(latex_code)
    
    print(f"LaTeX code generated and saved to {tex_filename}.")

    # Compile the LaTeX file twice using xelatex with nonstop mode
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename])
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex_filename])

    # Open the resulting PDF with evince
    subprocess.run(["evince", pdf_filename])

