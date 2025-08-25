import os
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def combine_pdfs(input_files, output_file):
    """
    Combine multiple PDF files into a single PDF file.
    Args:
        input_files (list): List of paths to input PDF files
        output_file (str): Path to an output PDF file
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        writer = PdfWriter()
        for input_file in input_files:
            if not os.path.exists(input_file):
                print(f"Warning: File not found: {input_file}")
                continue
            if not input_file.lower().endswith('.pdf'):
                print(f"Warning: Skipping non-PDF file: {input_file}")
                continue
            print(f"Adding: {input_file}")
            try:
                reader = PdfReader(input_file)
                for page in reader.pages:
                    writer.add_page(page)
            except Exception as e:
                print(f"Error reading {input_file}: {e}")
                continue
        if len(writer.pages) == 0:
            print("Error: No pages to write")
            return False
        with open(output_file, 'wb') as output:
            writer.write(output)
        print(
            f"Successfully combined {len(input_files)} files into: {output_file}"
        )
        print(f"Total pages: {len(writer.pages)}")
        return True
    except Exception as e:
        print(f"Error combining PDFs: {e}")
        return False


def get_pdf_files_from_directory(directory):
    """
    Get all PDF files from a directory.
    Args:
        directory (str): Path to directory
    Returns:
        list: List of PDF file paths
    """
    pdf_files = []
    for file in Path(directory).glob("*.pdf"):
        pdf_files.append(str(file))
    return sorted(pdf_files)


def main():
    """Main function to handle command line arguments and combine PDFs."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python pdf_combine.py output.pdf input1.pdf input2.pdf ...")
        print("  python pdf_combine.py output.pdf --directory /path/to/pdfs")
        print("Options:")
        print("  --directory DIR  Combine all PDF files from directory")
        print("Examples:")
        print("  python pdf_combine.py combined.pdf file1.pdf file2.pdf ...")
        print("  python pdf_combine.py all_pdfs.pdf --directory ./documents/")
        return
    output_file = sys.argv[1]
    if len(sys.argv) == 4 and sys.argv[2] == "--directory":
        directory = sys.argv[3]
        if not os.path.isdir(directory):
            print(f"Error: Directory not found: {directory}")
            return
        input_files = get_pdf_files_from_directory(directory)
        if not input_files:
            print(f"No PDF files found in directory: {directory}")
            return
        print(f"Found {len(input_files)} PDF files in directory")
    else:
        input_files = sys.argv[2:]
    valid_files = []
    for file in input_files:
        if os.path.exists(file) and file.lower().endswith('.pdf'):
            valid_files.append(file)
        else:
            print(f"Warning: Skipping invalid file: {file}")
    if not valid_files:
        print("Error: No valid PDF files to combine")
        return
    print(f"Combining {len(valid_files)} PDF files...")
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    success = combine_pdfs(valid_files, output_file)
    if success:
        print("✓ PDF combination completed successfully!")
    else:
        print("✗ PDF combination failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
