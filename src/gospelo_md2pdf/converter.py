"""Markdown to PDF conversion logic."""

import os
import shutil
from pathlib import Path

import markdown
from weasyprint import HTML, CSS

from .mermaid import process_mermaid_blocks
from .styles import get_default_css, load_css_file


def get_temp_dir(output_dir: Path) -> Path:
    """
    Get temporary directory for intermediate files (HTML, mermaid).

    Args:
        output_dir: The output directory for PDF

    Returns:
        Path to temporary directory (output_dir/tmp)
    """
    temp_dir = output_dir / "tmp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def get_output_dir(output_dir: str | Path | None = None) -> Path:
    """
    Get output directory from parameter, environment variable, or default.

    Priority:
    1. Explicit output_dir parameter
    2. MD2PDF_OUTPUT_DIR environment variable
    3. Current working directory

    Args:
        output_dir: Explicit output directory (optional)

    Returns:
        Path object for the output directory
    """
    if output_dir:
        return Path(output_dir)

    env_dir = os.environ.get("MD2PDF_OUTPUT_DIR")
    if env_dir:
        return Path(env_dir)

    return Path.cwd()


def convert_md_to_html(
    input_file: str | Path,
    output_dir: Path,
    css_file: str | Path | None = None,
    lang: str = "ja",
    verbose: bool = False,
) -> tuple[str, Path]:
    """
    Convert Markdown file to HTML with Mermaid diagram processing.

    Args:
        input_file: Path to input Markdown file
        output_dir: Directory to save HTML and assets
        css_file: Path to CSS file (optional, uses default if not provided)
        lang: HTML lang attribute (default: "ja")
        verbose: Whether to print verbose output

    Returns:
        Tuple of (HTML content, HTML file path)

    Raises:
        FileNotFoundError: If input file does not exist
    """
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    if verbose:
        print(f"Reading: {input_path}")

    # Read Markdown content
    md_content = input_path.read_text(encoding="utf-8")

    # Convert Markdown to HTML
    md = markdown.Markdown(
        extensions=[
            "tables",
            "fenced_code",
            "toc",
            "meta",
            "attr_list",
            "md_in_html",
        ]
    )
    html_body = md.convert(md_content)

    # Extract title from metadata or first h1
    title = "Document"
    if hasattr(md, "Meta") and "title" in md.Meta:
        title = md.Meta["title"][0]

    # Process Mermaid blocks
    if verbose:
        print("Processing Mermaid diagrams...")
    html_body = process_mermaid_blocks(html_body, output_dir, input_path.stem, verbose)

    # Prepare CSS content
    if css_file:
        css_content = load_css_file(css_file)
        if verbose:
            print(f"Using custom CSS: {css_file}")
    else:
        css_content = get_default_css()
        if verbose:
            print("Using default CSS")

    # Build complete HTML document
    html_content = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
{css_content}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save HTML file
    html_path = output_dir / (input_path.stem + ".html")
    html_path.write_text(html_content, encoding="utf-8")

    if verbose:
        print(f"HTML generated: {html_path}")

    return html_content, html_path


def convert_html_to_pdf(
    html_content: str,
    output_file: Path,
    css_file: str | Path | None = None,
    verbose: bool = False,
) -> Path:
    """
    Convert HTML content to PDF.

    Args:
        html_content: HTML content string
        output_file: Path to output PDF file
        css_file: Path to additional CSS file (optional)
        verbose: Whether to print verbose output

    Returns:
        Path to generated PDF file
    """
    stylesheets = []

    # Add external CSS if specified (in addition to embedded CSS)
    if css_file and Path(css_file).exists():
        stylesheets.append(CSS(filename=str(css_file)))

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Generate PDF
    if verbose:
        print(f"Generating PDF: {output_file}")

    HTML(string=html_content).write_pdf(
        output_file, stylesheets=stylesheets if stylesheets else None
    )

    return output_file


def convert_md_to_pdf(
    input_file: str | Path,
    output_file: str | Path | None = None,
    output_dir: str | Path | None = None,
    css_file: str | Path | None = None,
    keep_html: bool = True,
    lang: str = "ja",
    verbose: bool = False,
) -> Path:
    """
    Convert Markdown file to PDF.

    Args:
        input_file: Path to input Markdown file
        output_file: Path to output PDF file (optional, defaults to input_file.pdf)
        output_dir: Output directory (optional, uses env var or current dir)
        css_file: Path to CSS file (optional, uses default if not provided)
        keep_html: Whether to keep the intermediate HTML file (default: True)
        lang: HTML lang attribute (default: "ja")
        verbose: Whether to print verbose output

    Returns:
        Path to generated PDF file

    Raises:
        FileNotFoundError: If input file does not exist
    """
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Determine output directory
    resolved_output_dir = get_output_dir(output_dir)
    resolved_output_dir.mkdir(parents=True, exist_ok=True)

    # Get temporary directory for intermediate files
    temp_dir = get_temp_dir(resolved_output_dir)

    # Determine output PDF filename
    if output_file is None:
        pdf_path = resolved_output_dir / (input_path.stem + ".pdf")
    else:
        output_path_obj = Path(output_file)
        if not output_path_obj.is_absolute():
            pdf_path = resolved_output_dir / output_path_obj
        else:
            pdf_path = output_path_obj

    # Step 1: Convert Markdown to HTML (with Mermaid processing)
    # Use temp_dir for intermediate HTML and mermaid files
    html_content, html_path = convert_md_to_html(
        input_file, temp_dir, css_file, lang, verbose
    )

    # Step 2: Convert HTML to PDF
    convert_html_to_pdf(html_content, pdf_path, css_file, verbose)

    # Clean up intermediate files
    if not keep_html:
        # Remove entire temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            if verbose:
                print(f"Removed intermediate files: {temp_dir}")
    else:
        # Keep HTML but still note location
        if verbose:
            print(f"Intermediate files saved in: {temp_dir}")

    return pdf_path
