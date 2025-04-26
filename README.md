# PDF to HTML OCR Converter

A Python utility that converts scanned PDF documents into searchable HTML files using Optical Character Recognition (OCR) technology. The tool processes each page of the PDF, extracts text using Tesseract OCR, and generates a clean, readable HTML output.

## Features

- Converts scanned PDFs to searchable HTML format
- Processes multiple pages with automatic page numbering
- Preserves text structure with proper HTML formatting
- Handles UTF-8 encoding for international character support
- Includes proper HTML escaping for special characters

## Prerequisites

- Python 3.x
- Tesseract OCR
- Poppler utilities
- Python packages:
  - pdf2image
  - pytesseract

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-to-html.git
cd pdf-to-html
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install the required Python packages:
```bash
pip install pdf2image pytesseract
```

4. Install Tesseract OCR:
- **macOS**: `brew install tesseract`
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **Windows**: Download and install from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

5. Install Poppler:
- **macOS**: `brew install poppler`
- **Ubuntu/Debian**: `sudo apt-get install poppler-utils`
- **Windows**: Download from [poppler releases](http://blog.alivate.com.au/poppler-windows/)

## Usage

Run the script from the command line:

```bash
python ocr_to_html.py input.pdf output.html
```

Replace `input.pdf` with the path to your scanned PDF file and `output.html` with your desired output HTML file name.

### Example:
```bash
python ocr_to_html.py daily-stoic.pdf daily-stoic.html
```

## Configuration

The script accepts the following optional parameters in the `pdf_to_html_ocr` function (not the command line):

- `dpi`: Resolution for PDF conversion (default: 300)
- `poppler_path`: Custom path to poppler binaries (if needed)

## Output Format

The generated HTML file includes:
- UTF-8 encoding
- Page numbers as headers
- Paragraphs for each line of text
- Escaped special characters
- Clean, semantic HTML structure

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [pytesseract](https://github.com/madmaze/pytesseract) 