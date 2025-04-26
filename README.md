# PDF to HTML OCR Converter

A Python utility that converts scanned PDF documents into searchable HTML files using Optical Character Recognition (OCR) technology. The tool processes each page of the PDF, extracts text using Tesseract OCR, and generates a clean, readable HTML output with intelligent paragraph formatting.

## Features

- Converts scanned PDFs to searchable HTML format
- Processes multiple pages with automatic page numbering
- Preserves text structure with proper HTML formatting
- Handles UTF-8 encoding for international character support
- Includes proper HTML escaping for special characters
- Intelligent paragraph reconstruction:
  - Combines line breaks that occur due to page width
  - Preserves natural sentence boundaries
  - Maintains proper paragraph separation
  - Handles hyphenated words at line breaks
  - Preserves short text blocks like titles and headings

## Prerequisites

- Python 3.x
- Tesseract OCR
- Poppler utilities
- Python packages:
  - pdf2image
  - pytesseract
  - beautifulsoup4

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
pip install -r requirements.txt
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

The conversion process involves two steps:

1. First, convert the PDF to HTML with OCR:
```bash
python ocr_to_html.py input.pdf intermediate.html
```

2. Then, fix the paragraph formatting:
```bash
python html_paragraph_fixer.py intermediate.html output.html
```

You can also process files in one step by piping them together:
```bash
python ocr_to_html.py input.pdf intermediate.html && python html_paragraph_fixer.py intermediate.html output.html
```

Replace `input.pdf` with the path to your scanned PDF file and `output.html` with your desired output HTML file name.

### Example:
```bash
python ocr_to_html.py daily-stoic.pdf daily-stoic-raw.html
python html_paragraph_fixer.py daily-stoic-raw.html daily-stoic.html
```

## Configuration

The OCR script (`ocr_to_html.py`) accepts the following optional parameters in the `pdf_to_html_ocr` function:
- `dpi`: Resolution for PDF conversion (default: 300)
- `poppler_path`: Custom path to poppler binaries (if needed)

The paragraph fixer (`html_paragraph_fixer.py`) uses intelligent heuristics to determine paragraph boundaries:
- Preserves sentences that end with proper punctuation
- Combines lines that were split due to page width
- Maintains separation for headings and titles
- Handles hyphenated words at line breaks
- Respects natural sentence capitalization

## Output Format

The generated HTML file includes:
- UTF-8 encoding
- Page numbers as headers
- Properly formatted paragraphs with natural text flow
- Escaped special characters
- Clean, semantic HTML structure
- Preserved formatting for titles and headings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [pytesseract](https://github.com/madmaze/pytesseract)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) 