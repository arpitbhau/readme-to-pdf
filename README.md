# README to PDF Converter

A powerful tool to convert Markdown README files to PDF with GitHub's dark theme styling. Perfect for creating beautiful documentation PDFs from your project's README.

## Features

- Converts Markdown to HTML with GitHub's dark theme
- Properly handles images with relative paths (e.g., `./img/some.jpg`)
- Maintains directory structure for images in output
- Converts the HTML to PDF with proper formatting
- Maintains the exact look and feel of the original README
- Command-line interface with customizable styling options

## Requirements

- Python 3.6+
- WeasyPrint (required for PDF conversion)

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Install WeasyPrint dependencies:
   - On Ubuntu/Debian: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`
   - On macOS: `brew install pango`
   - On Windows: No additional dependencies required

## Usage

### Basic Usage

Convert a Markdown file to PDF with default GitHub dark theme:

```bash
python md2pdf.py md-to-pdf README.md
```

### Project Structure

The tool works best with this project structure:
```
project/
├── README.md
├── img/              # Images directory
│   ├── image1.jpg
│   └── image2.png
├── docs/             # Documentation images
│   └── diagram.svg
└── md2pdf.py
```

Images in your README.md can be referenced like this:
```markdown
![Image 1](./img/image1.jpg)
![Diagram](./docs/diagram.svg)
```

### Customizing Output

Convert a Markdown file to PDF with custom styling:

```bash
python md2pdf.py md-to-pdf README.md --output="custom.pdf" --bg-color="#000000" --text-color="#ffffff"
```

### Available Commands

1. **md-to-pdf**: Convert Markdown to PDF
   ```bash
   python md2pdf.py md-to-pdf [input_file] [options]
   ```

2. **md-to-html**: Convert Markdown to HTML
   ```bash
   python md2pdf.py md-to-html [input_file] [options]
   ```

3. **html-to-pdf**: Convert HTML to PDF
   ```bash
   python md2pdf.py html-to-pdf [input_file] [options]
   ```

### Command Options

#### Common Options for md-to-pdf and md-to-html

- `--output`, `-o`: Output file path (default: output.pdf or output.html)
- `--bg-color`: Background color (default: #0d1117 - GitHub dark theme)
- `--text-color`: Text color (default: #c9d1d9 - GitHub dark theme)
- `--heading-color`: Heading color (default: #e6f1ff - GitHub dark theme)
- `--link-color`: Link color (default: #58a6ff - GitHub dark theme)
- `--code-bg`: Code block background color (default: #161b22 - GitHub dark theme)
- `--border-color`: Border color (default: #30363d - GitHub dark theme)
- `--no-images`: Skip copying images to output directory

#### Additional Options for md-to-pdf and html-to-pdf

- `--page-size`: Page size (default: A4)
- `--margin`: Page margin (default: 10mm)

### Examples

1. Convert README.md to PDF with black background:
   ```bash
   python md2pdf.py md-to-pdf README.md --bg-color="#000000" --output="dark.pdf"
   ```

2. Convert README.md to HTML with light theme:
   ```bash
   python md2pdf.py md-to-html README.md --bg-color="#ffffff" --text-color="#24292e" --output="light.html"
   ```

3. Convert HTML to PDF with custom page size:
   ```bash
   python md2pdf.py html-to-pdf output.html --page-size="Letter" --margin="20mm"
   ```

## Image Handling

The tool automatically:
- Detects images in your Markdown/HTML
- Handles relative paths (e.g., `./img/photo.jpg`, `../docs/image.png`)
- Maintains the same directory structure in the output
- Copies images to the correct location in the output directory

## Customization

You can modify the styling in the `generate_html_template` function to change the appearance of the generated HTML and PDF.

## Deactivating Virtual Environment

When you're done using the application, you can deactivate the virtual environment:

```bash
deactivate
``` 