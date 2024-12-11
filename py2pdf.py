import textwrap

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


FONT = "Microsoft YaHei"
FONT_PATH = "C:\\Windows\\Fonts\\msyh.ttc"
FONT_SIZE = 10
LINE_HEIGHT = 14
LINE_WIDTH = 110


def python_to_pdf(input_file, output_file, header):
    # Register a font that supports Chinese characters
    pdfmetrics.registerFont(TTFont(FONT, FONT_PATH))

    # Open the Python file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Create a PDF canvas
    pdf = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    pdf.setFont(FONT, FONT_SIZE)

    # Initialize Y-coordinate for writing content
    y = height - 70
    current_page = 1

    def draw_header():
        """Draw the header on each page."""
        pdf.setFont(FONT, FONT_SIZE)
        pdf.drawString(50, height - 30, header)  # Page header
        pdf.drawRightString(width - 50, height - 30, f"{current_page}")  # Page number

    draw_header()

    # Write lines with wrapping and pagination
    for line in lines:
        stripped_line = line.rstrip('\n')  # Remove trailing newline character

        # Handle blank lines
        if stripped_line.strip() == "":
            if y < 50:  # Start a new page if not enough space
                pdf.showPage()
                current_page += 1
                draw_header()
                y = height - 70

            # Add space for a blank line
            y -= LINE_HEIGHT
            continue

        # Wrap lines exceeding the width
        wrapped_lines = textwrap.wrap(stripped_line, LINE_WIDTH)

        for wrapped_line in wrapped_lines:
            if y < 50:  # Start a new page if not enough space
                pdf.showPage()
                current_page += 1
                draw_header()
                y = height - 70

            # Write the wrapped line to the PDF
            pdf.drawString(50, y, wrapped_line)
            y -= LINE_HEIGHT

    # Finalize the document
    pdf.save()
    print(f"Converted {input_file} to {output_file}")


# Specify input and output files
python_file = "cli.py"  # Replace with your Python file
pdf_file = "cli.pdf"
page_header = "DMP数据筛选流水线 1.0"   # Replace with desired PDF file name

# Call the function
python_to_pdf(python_file, pdf_file, page_header)
