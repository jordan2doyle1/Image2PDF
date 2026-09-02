# Image2PDF

A simple Python CLI for converting JPEG/JPG/PNG images to PDF files.

## Requirements

- Python 3.9+
- [img2pdf](https://pypi.org/project/img2pdf/)

## Usage

Convert a single file:

```bash
python3 image2pdf.py image.jpg
```

Combine all images in a directory into one PDF:

```bash
python3 image2pdf.py ./my_images/
```

## Behavior

- **Supported formats:** `.jpg`, `.jpeg`, `.png`
- **Single file mode:** converts the file to a single-page PDF alongside the original.
- **Directory mode:** combines all supported images (alphabetically) into one PDF named `<directory>.pdf` inside that directory.

## Constraints

- Original files are never modified or deleted.
- Existing output PDFs are never overwritten — the tool will log an error and skip.
