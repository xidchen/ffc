from typing import Any, Dict, Protocol, Tuple, cast

import pymupdf


class PageProto(Protocol):
    def draw_rect(
        self,
        rect: "pymupdf.Rect",
        color: Tuple[float, float, float] | None = None,
        fill: Tuple[float, float, float] | None = None,
    ) -> None: ...
    def get_text(self, mode: str) -> Dict[str, Any]: ...
    def add_redact_annot(self, rect: "pymupdf.Rect") -> None: ...
    def apply_redactions(self) -> None: ...


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
        doc = pymupdf.open(input_pdf_path)
        for page_num in range(len(doc)):
            page = cast(PageProto, doc[page_num])
            header_rect = pymupdf.Rect(0, 0, header_width, header_height)
            page.draw_rect(header_rect, color=(1, 1, 1), fill=(1, 1, 1))
            text_instances = page.get_text("dict")
            for block in text_instances["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if (span["bbox"][0] < header_width
                                    and span["bbox"][1] < header_height):
                                rect = pymupdf.Rect(span["bbox"])
                                page.add_redact_annot(rect)
            page.apply_redactions()
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
        doc = pymupdf.open(input_pdf_path)
        for page_num in range(len(doc)):
            page = cast(PageProto, doc[page_num])
            blocks = page.get_text("blocks")
            for block in blocks:
                x0, y0, x1, y1 = block[:4]
                if float(x0) < header_width and float(y0) < header_height:
                    rect = pymupdf.Rect(x0, y0, x1, y1)
                    page.add_redact_annot(rect)
            page.apply_redactions()
        doc.save(output_pdf_path)
        doc.close()
        print(f"Headers removed successfully using alternative method")
        return True
    except Exception as e:
        print(f"Error in alternative method: {str(e)}")
        return False


if __name__ == "__main__":
    input_file = input("Input file path: ")
    output_file = input("Output file path: ")
    success = remove_upper_left_header(
        input_pdf_path=input_file,
        output_pdf_path=output_file,
        header_height=30,
        header_width=250,
    )
    if not success:
        print("Trying alternative method...")
        remove_upper_left_header_alternative(
            input_pdf_path=input_file,
            output_pdf_path=output_file,
            header_height=30,
            header_width=250,
        )
