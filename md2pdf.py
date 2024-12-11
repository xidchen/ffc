from markdown import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.units import inch


def markdown_to_pdf(input_file, output_file):
    # Read the Markdown content
    with open(input_file, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # Convert Markdown to HTML
    html_content = markdown(md_content)

    # Create a PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Split HTML into paragraphs
    for line in html_content.split("\n"):
        if line.strip():
            paragraph = Paragraph(line, styles['BodyText'])
            elements.append(paragraph)
            elements.append(Spacer(1, 0.2 * inch))  # Add space between lines

    # Build the PDF
    doc.build(elements)
    print(f"Converted {input_file} to {output_file}")


# Specify the input and output files
markdown_file = "README.md"  # Replace with your Markdown file
pdf_file = "README.pdf"  # Replace with the desired PDF file name

# Convert Markdown to PDF
markdown_to_pdf(markdown_file, pdf_file)
