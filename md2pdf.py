#!/usr/bin/env python3
# Jai Shree Ram

import pdfkit
from bs4 import BeautifulSoup
import os
import markdown2
import re
import shutil
import argparse
import sys


def parse_arguments():
    """
    Parse command line arguments
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Convert Markdown to PDF with GitHub dark theme')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Common arguments for all commands
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('input', help='Input file path')
    common_parser.add_argument('--output', '-o', help='Output file path')
    common_parser.add_argument('--bg-color', default='#0d1117', help='Background color')
    common_parser.add_argument('--text-color', default='#c9d1d9', help='Text color')
    common_parser.add_argument('--heading-color', default='#e6f1ff', help='Heading color')
    common_parser.add_argument('--link-color', default='#58a6ff', help='Link color')
    common_parser.add_argument('--code-bg', default='#161b22', help='Code block background color')
    common_parser.add_argument('--border-color', default='#30363d', help='Border color')
    common_parser.add_argument('--no-images', action='store_true', help='Skip copying images')
    
    # md-to-pdf command
    md_to_pdf = subparsers.add_parser('md-to-pdf', parents=[common_parser])
    md_to_pdf.add_argument('--page-size', default='A4', help='Page size')
    md_to_pdf.add_argument('--margin', default='10mm', help='Page margin')
    
    # md-to-html command
    subparsers.add_parser('md-to-html', parents=[common_parser])
    
    # html-to-pdf command
    html_to_pdf = subparsers.add_parser('html-to-pdf', parents=[common_parser])
    html_to_pdf.add_argument('--page-size', default='A4', help='Page size')
    html_to_pdf.add_argument('--margin', default='10mm', help='Page margin')
    
    return parser.parse_args()


def copy_images(html_content, input_file, output_dir, no_images=False):
    """
    Copy images from the original assets directory to the new assets directory
    Args:
        html_content (str): HTML content
        input_file (str): Path to input Markdown file
        output_dir (str): Path to output directory
        no_images (bool): Whether to skip copying images
    Returns:
        str: Updated HTML content with image paths updated
    """
    if no_images:
        return html_content
    
    # Get the directory of the input file
    input_dir = os.path.dirname(os.path.abspath(input_file))
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Find all image tags in the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')

    for img in img_tags:
        src = img.get('src')
        if src:
            # Handle relative paths
            if src.startswith('./'):
                src = src[2:]  # Remove './'
            elif src.startswith('../'):
                # Handle parent directory references
                src = os.path.normpath(os.path.join(input_dir, src))

            # Get absolute path of the image
            img_path = os.path.join(input_dir, src)
            
            if os.path.exists(img_path):
                # Create the same directory structure in output
                rel_path = os.path.dirname(src)
                if rel_path:
                    os.makedirs(os.path.join(output_dir, rel_path), exist_ok=True)
                
                # Copy the image
                shutil.copy2(img_path, os.path.join(output_dir, src))
                
                # Update the image source in HTML
                img['src'] = src

    return str(soup)


def generate_html_template(html_content, bg_color, text_color, heading_color, link_color, code_bg, border_color):
    """
    Generate HTML template with GitHub dark theme
    Args:
        html_content (str): HTML content
        bg_color (str): Background color
        text_color (str): Text color
        heading_color (str): Heading color
        link_color (str): Link color
        code_bg (str): Code block background color
        border_color (str): Border color
    Returns:
        str: Complete HTML template
    """
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: {bg_color};
                color: {text_color};
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: {heading_color};
                margin-top: 24px;
                margin-bottom: 16px;
                font-weight: 600;
                line-height: 1.25;
            }}
            a {{
                color: {link_color};
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            code {{
                background-color: {code_bg};
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            }}
            pre {{
                background-color: {code_bg};
                padding: 16px;
                border-radius: 6px;
                overflow: auto;
            }}
            pre code {{
                background-color: transparent;
                padding: 0;
            }}
            img {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 16px;
            }}
            th, td {{
                border: 1px solid {border_color};
                padding: 6px 13px;
            }}
            th {{
                background-color: {code_bg};
            }}
            blockquote {{
                padding: 0 1em;
                color: {text_color};
                border-left: 0.25em solid {border_color};
                margin: 0 0 16px 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''


def convert_markdown_to_html(input_file, bg_color, text_color, heading_color, link_color, code_bg, border_color):
    """
    Convert Markdown file to HTML with GitHub dark theme
    Args:
        input_file (str): Path to input Markdown file
        bg_color (str): Background color
        text_color (str): Text color
        heading_color (str): Heading color
        link_color (str): Link color
        code_bg (str): Code block background color
        border_color (str): Border color
    Returns:
        str: Complete HTML content
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # Convert markdown to HTML
    html = markdown2.markdown(markdown_text, extras=['fenced-code-blocks', 'tables'])

    # Generate HTML template with GitHub dark theme
    html_template = generate_html_template(html, bg_color, text_color, heading_color, link_color, code_bg, border_color)

    return html_template


def convert_html_to_pdf(html_file, output_file, page_size, margin):
    """
    Convert HTML file to PDF using pdfkit
    Args:
        html_file (str): Path to input HTML file
        output_file (str): Path to output PDF file
        page_size (str): Page size
        margin (str): Page margin
    """
    options = {
        'page-size': page_size,
        'margin-top': margin,
        'margin-right': margin,
        'margin-bottom': margin,
        'margin-left': margin,
        'encoding': 'UTF-8',
        'no-outline': None
    }
    pdfkit.from_file(html_file, output_file, options=options)


def main():
    """
    Main function
    """
    args = parse_arguments()
    
    # Check if wkhtmltopdf is installed
    try:
        pdfkit.from_string('', 'test.pdf')
    except OSError:
        print("Error: wkhtmltopdf is not installed. Please install it first.")
        print("On Ubuntu/Debian: sudo apt-get install wkhtmltopdf")
        print("On macOS: brew install wkhtmltopdf")
        print("On Windows: Download from https://wkhtmltopdf.org/downloads.html")
        sys.exit(1)
    
    # Set default output file names
    if not args.output:
        if args.command == 'md-to-pdf':
            args.output = 'output.pdf'
        elif args.command == 'md-to-html':
            args.output = 'output.html'
        elif args.command == 'html-to-pdf':
            args.output = 'output.pdf'

    # Create output directory for images
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if not output_dir:
        output_dir = '.'

    if args.command == 'md-to-pdf':
        # Convert markdown to HTML
        html_content = convert_markdown_to_html(
            args.input,
            args.bg_color,
            args.text_color,
            args.heading_color,
            args.link_color,
            args.code_bg,
            args.border_color
        )

        # Copy images and update HTML
        html_content = copy_images(html_content, args.input, output_dir, args.no_images)

        # Save HTML temporarily
        temp_html = 'temp.html'
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Convert HTML to PDF
        convert_html_to_pdf(temp_html, args.output, args.page_size, args.margin)

        # Clean up temporary HTML file
        os.remove(temp_html)

    elif args.command == 'md-to-html':
        # Convert markdown to HTML
        html_content = convert_markdown_to_html(
            args.input,
            args.bg_color,
            args.text_color,
            args.heading_color,
            args.link_color,
            args.code_bg,
            args.border_color
        )

        # Copy images and update HTML
        html_content = copy_images(html_content, args.input, output_dir, args.no_images)

        # Save HTML
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)

    elif args.command == 'html-to-pdf':
        # Copy images and update HTML
        with open(args.input, 'r', encoding='utf-8') as f:
            html_content = f.read()
        html_content = copy_images(html_content, args.input, output_dir, args.no_images)

        # Save updated HTML temporarily
        temp_html = 'temp.html'
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Convert HTML to PDF
        convert_html_to_pdf(temp_html, args.output, args.page_size, args.margin)

        # Clean up temporary HTML file
        os.remove(temp_html)


if __name__ == "__main__":
    main() 