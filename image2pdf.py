"""Convert and combine JPEG/PNG images to single PDF file.

Usage:
    python image2pdf.py <file_or_directory>

Single file mode converts the image to a single-page PDF.
Directory mode combines all supported images into one PDF.
"""

import argparse
import logging
import os

import img2pdf


def convert_directory(directory_path):
    """Combine all supported images in a directory into a single PDF.

    Images are sorted alphabetically. The output PDF is written to
    <directory_name>.pdf inside the given directory. Skips if no supported files
    are found or if the output already exists.

    Args:
        directory_path: Path to the directory containing images.
    """
    directory_name = os.path.basename(directory_path)
    output_file = os.path.join(directory_path, f"{directory_name}.pdf")

    files = sorted(
        f for f in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, f))
        and os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    )

    if not files:
        logging.error(f"No supported image files found in: {directory_path}")
        return

    if os.path.isfile(output_file):
        logging.error(f"Output file already exists, skipping: {output_file}")
        return

    logging.info(f"Found {len(files)} image(s) in: {directory_path}")
    logging.info(f"Combining into: {output_file}")

    file_paths = [os.path.join(directory_path, f) for f in files]

    with open(output_file, "wb") as f:
        f.write(img2pdf.convert(file_paths))
    logging.info(f"Created: {output_file}")


def convert_file(file_path):
    """Convert a single image file to a PDF.

    The output is written alongside the original with a .pdf extension. Skips
    unsupported file types or if the output already exists.

    Args:
        file_path: Path to the image file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        logging.error(f"Skipping unsupported file type: {file_path}")
        return

    base_path = os.path.splitext(file_path)[0]
    output_file = f"{base_path}.pdf"

    if os.path.isfile(output_file):
        logging.error(f"Output file already exists, skipping: {output_file}")
        return

    with open(output_file, "wb") as f:
        f.write(img2pdf.convert(file_path))
    logging.info(f"Created: {output_file}")


USAGE_DESCRIPTION = """
Converts JPEG/JPG/PNG images to PDF files.

    - Single file: converts to a single-page PDF.
    - Directory: combines all images into one PDF.

Original files are preserved.
"""

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

parser = argparse.ArgumentParser(description=USAGE_DESCRIPTION)
parser.add_argument('input_path',
                    help="Input file or directory to be converted.")
args = parser.parse_args()

log_format = '[%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

if not os.path.exists(args.input_path):
    logging.error(f"Path \'{args.input_path}\' does not exist")
    exit(2)

if os.path.isfile(args.input_path):
    convert_file(args.input_path)
elif os.path.isdir(args.input_path):
    convert_directory(args.input_path)
