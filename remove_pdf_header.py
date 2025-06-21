import fitz


def remove_upper_left_header(
        input_pdf_path, output_pdf_path, header_height=50, header_width=200
):
    """
    Remove header content from the upper left side of each page in a PDF file.

    Args:
        input_pdf_path (str): Path to the input PDF file
        output_pdf_path (str): Path to save the modified PDF file
        header_height (float): Height of the header area to remove (in points)
        header_width (float): Width of the header area to remove (in points)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Open the PDF file
        doc = fitz.open(input_pdf_path)

        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Define the header area to remove (an upper left corner)
            header_rect = fitz.Rect(0, 0, header_width, header_height)

            # Create a white rectangle to cover the header area
            page.draw_rect(header_rect, color=(1, 1, 1), fill=(1, 1, 1))

            # Alternative approach: Remove all text/content in the header area
            # This is more thorough but might be slower
            text_instances = page.get_text("dict")
            for block in text_instances["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            # Check if a text is in the header area
                            if (span["bbox"][0] < header_width and span["bbox"][
                                1] < header_height):
                                # Create a redaction annotation to remove the text
                                rect = fitz.Rect(span["bbox"])
                                page.add_redact_annot(rect)

            # Apply redactions
            page.apply_redactions()

        # Save the modified PDF
        doc.save(output_pdf_path)
        doc.close()

        print(f"Successfully removed headers from {input_pdf_path}")
        print(f"Modified PDF saved as {output_pdf_path}")
        return True

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return False


def remove_upper_left_header_alternative(
        input_pdf_path, output_pdf_path, header_height=50, header_width=200
):
    """
    Alternative approach using content stream manipulation for more precise removal.

    Args:
        input_pdf_path (str): Path to the input PDF file
        output_pdf_path (str): Path to save the modified PDF file
        header_height (float): Height of the header area to remove (in points)
        header_width (float): Width of the header area to remove (in points)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        doc = fitz.open(input_pdf_path)

        for page_num in range(len(doc)):
            page = doc[page_num]

            # Get all text blocks
            blocks = page.get_text("blocks")


            # Remove text blocks that fall within the header area
            for block in blocks:
                x0, y0, x1, y1 = block[:4]

                # Check if the block is in the upper left header area
                if x0 < header_width and y0 < header_height:
                    # Create a redaction rectangle for this block
                    rect = fitz.Rect(x0, y0, x1, y1)
                    page.add_redact_annot(rect)

            # Apply all redactions
            page.apply_redactions()

        # Save the result
        doc.save(output_pdf_path)
        doc.close()

        print(f"Headers removed successfully using alternative method")
        return True

    except Exception as e:
        print(f"Error in alternative method: {str(e)}")
        return False


# Example usage
if __name__ == "__main__":
    # Example usage
    input_file = input("Input file path: ")
    output_file = input("Output file path: ")

    # Method 1: White rectangle overlay
    success = remove_upper_left_header(input_pdf_path=input_file,
        output_pdf_path=output_file, header_height=30,
        # Adjust based on your header size
        header_width=250  # Adjust based on your header size
    )

    if not success:
        # Try alternative method if the first one fails
        print("Trying alternative method...")
        remove_upper_left_header_alternative(input_pdf_path=input_file,
            output_pdf_path=output_file, header_height=30, header_width=250)
