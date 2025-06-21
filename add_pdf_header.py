import io
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter


def add_header_to_pdf(input_pdf_path, output_pdf_path, name):
    """
    Add a header with name and page number to each page of a PDF

    Args:
        input_pdf_path (str): Path to the input PDF file
        output_pdf_path (str): Path to save the output PDF file
        name (str): Name to add in the header
    """
    # Set up font - using common CJK fonts available on Ubuntu
    cjk_font_paths = [
        "/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf",
        "/usr/share/fonts/truetype/arphic-gkai00mp/gkai00mp.ttf",
        "C:\\Windows\\Fonts\\msyh.ttc",
        "C:\\Windows\\Fonts\\simsun.ttc",
    ]

    font_name = "CJKFont"
    font_path = None

    # Find the first available CJK font
    for path in cjk_font_paths:
        if os.path.exists(path):
            font_path = path
            break

    if not font_path:
        print("Warning: No CJK font found. Falling back to Helvetica.")
        font_name = "Helvetica"
    else:
        # Register the CJK font
        pdfmetrics.registerFont(TTFont(font_name, font_path))

    # Read the input PDF
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()

    # Process each page
    for page_num, page in enumerate(pdf_reader.pages):
        # Get page size
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        # Create header content using reportlab
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=(page_width, page_height))

        # Set the font to regular (not bold)
        can.setFont(font_name, 10)

        # Add the name to the top left
        can.drawString(30, page_height - 30, name)

        # Add page number to top right - simplified to just current page number
        page_number_text = f"{page_num + 1}"
        can.drawString(page_width - 30, page_height - 30, page_number_text)

        can.save()

        # Move to the beginning of the BytesIO buffer
        packet.seek(0)

        # Create a new PDF with the header
        watermark = PdfReader(packet)
        watermark_page = watermark.pages[0]

        # Merge the watermark with the page
        page.merge_page(watermark_page)

        # Add the page to the output PDF
        pdf_writer.add_page(page)

    # Save the output PDF
    with open(output_pdf_path, "wb") as output_file:
        pdf_writer.write(output_file)

    print(f"Headers added successfully. Output saved to {output_pdf_path}")


def main():
    print("=== PDF Header Adder ===")
    input_pdf_path = input("Enter the path to the input PDF file: ")
    output_pdf_path = input("Enter the path to save the output PDF file: ")
    name = input("Enter the name to add to the header: ")

    add_header_to_pdf(input_pdf_path, output_pdf_path, name)


if __name__ == "__main__":
    main()