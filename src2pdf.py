import os
import textwrap

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


SRC_DIR = os.path.join("vst_lite", "src")
OUT_DIR = os.path.join("vst_lite", "tgt")
OUT_FILE = os.path.join(OUT_DIR, "软著代码.pdf")

PAGE_SIZE = letter
MARGIN_LEFT = 40
MARGIN_TOP = 70
MARGIN_BOTTOM = 50
CHARS_PER_LINE = 100
LINES_PER_PAGE = 54
LINE_SPACING = 1.15
MIN_FONT_SIZE = 6
MAX_FONT_SIZE = 14
FONT_SCALE = 1.08
FONT_NAME_CODE = "Courier"


def gather_source_files(root):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            # include all files found
            files.append(os.path.join(dirpath, fn))
    return sorted(files)


def read_lines_no_blank(path):
    raw = None
    lines = []
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                raw = f.readlines()
            break
        except (UnicodeDecodeError, OSError):
            raw = None
            continue
    if raw is None:
        return []
    for line in raw:
        if line.strip() == "":
            continue
        lines.append(line.rstrip("\n"))
    return lines


def ensure_out_dir(path):
    os.makedirs(path, exist_ok=True)


def create_pdf(file_paths, out_pdf):
    pdf = canvas.Canvas(out_pdf, pagesize=PAGE_SIZE)
    width, height = PAGE_SIZE

    y_start = height - MARGIN_TOP

    available_height = y_start - MARGIN_BOTTOM
    # Compute a font size that fits LINES_PER_PAGE lines into available_height
    computed_font_size = int(available_height / (LINES_PER_PAGE * LINE_SPACING))
    # Optionally scale a little larger by default
    computed_font_size *= FONT_SCALE
    # Clamp to sensible bounds
    computed_font_size = max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, computed_font_size))
    # Round to one decimal for cleaner rendering
    font_size_for_pages = round(computed_font_size, 1)
    line_height = font_size_for_pages * LINE_SPACING

    # Start first page and set code font (no header or page numbers)
    pdf.setFont(FONT_NAME_CODE, font_size_for_pages)

    y = y_start
    line_count = 0  # lines written on the current page

    for path in file_paths:
        lines = read_lines_no_blank(path)
        if not lines:
            # skip files with no non-blank lines
            continue

        for raw_line in lines:
            # Wrap the line into pieces based on character count (not page width)
            wrapped = textwrap.wrap(raw_line, CHARS_PER_LINE) or [""]

            for part in wrapped:
                # Start a new page when we've reached the per-page line limit
                if line_count >= LINES_PER_PAGE:
                    pdf.showPage()
                    pdf.setFont(FONT_NAME_CODE, font_size_for_pages)
                    y = y_start
                    line_count = 0

                # Draw the code line (no header or page number)
                pdf.drawString(MARGIN_LEFT, y, part)
                y -= line_height
                line_count += 1

    pdf.save()
    print(f"Wrote combined PDF: {out_pdf}")


def main():
    if not os.path.isdir(SRC_DIR):
        print(f"Source directory not found: {SRC_DIR}")
        return
    ensure_out_dir(OUT_DIR)
    files = gather_source_files(SRC_DIR)
    if not files:
        print("No files found in source directory.")
        return
    create_pdf(files, OUT_FILE)


if __name__ == "__main__":
    main()
