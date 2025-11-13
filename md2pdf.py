from markdown import markdown
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageTemplate, Frame
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


FONT = "Microsoft YaHei"
FONT_PATH = "C:\\Windows\\Fonts\\msyh.ttc"
FONT_SIZE = 10
LINE_HEIGHT = 14
LINE_WIDTH = 110


def markdown_to_pdf(md_file, pdf_file, header):
    # Register a font supporting Unicode (if needed for special characters)
    pdfmetrics.registerFont(TTFont(FONT, FONT_PATH))

    # Page settings
    width, height = letter
    margin = 50

    def draw_header(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT, FONT_SIZE)
        # Add the title to the left
        canvas.drawString(margin, height - 30, header)
        # Add the page number to the right
        canvas.drawRightString(width - margin, height - 30, f"{doc.page}")
        canvas.restoreState()

    # Set up the document with a custom template
    frame = Frame(margin, margin, width - 2 * margin, height - 80, id='normal')
    template = PageTemplate(id='header_template', frames=[frame], onPage=draw_header)
    pdf = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=margin, leftMargin=margin,
                            topMargin=margin, bottomMargin=margin)
    pdf.addPageTemplates([template])

    # Read and convert Markdown to HTML
    with open(md_file, 'r', encoding='utf-8') as file:
        md_content = file.read()
    html_content = markdown(md_content)

    # Create the styles and content
    styles = getSampleStyleSheet()
    content = []

    for line in html_content.split("\n"):
        if line.strip():  # Skip empty lines
            paragraph = Paragraph(line, styles['BodyText'])
            content.append(paragraph)
            content.append(Spacer(1, 12))  # Add space between paragraphs

    # Build the PDF
    pdf.build(content, onFirstPage=draw_header, onLaterPages=draw_header)
    print(f"Converted {md_file} to {pdf_file}")

# Specify the input Markdown file and the output PDF file
markdown_file = input("Input file path: ")  # Input your Markdown file path
output_pdf = input("Output file path: ")  # Input your PDF file path
page_header = input("Page header name: ")  # Input your desired PDF file name

# Convert Markdown to PDF with a header
markdown_to_pdf(markdown_file, output_pdf, page_header)
