"""Command-line interface for gospelo-md2pdf."""

import argparse
import sys

from . import __version__
from .converter import convert_md_to_pdf


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        prog="gospelo-md2pdf",
        description="Convert Markdown to PDF with Japanese support and MermaidJS diagrams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    gospelo-md2pdf report.md
    gospelo-md2pdf report.md output.pdf
    gospelo-md2pdf report.md -o ./pdf
    gospelo-md2pdf report.md --css custom-style.css
    gospelo-md2pdf report.md --debug

Environment Variables:
    MD2PDF_OUTPUT_DIR    Output directory (lower priority than --output-dir)

Mermaid Support:
    To render Mermaid diagrams, install mermaid-cli:
    npm install -g @mermaid-js/mermaid-cli

Japanese Font:
    For Japanese text, install Noto Sans CJK JP:
    macOS:  brew install font-noto-sans-cjk-jp
    Ubuntu: sudo apt install fonts-noto-cjk
        """,
    )

    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", nargs="?", help="Output PDF file (optional)")
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Output directory (default: current directory or MD2PDF_OUTPUT_DIR env var)",
    )
    parser.add_argument("-c", "--css", help="Custom CSS file")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Keep intermediate files (HTML, mermaid) in tmp/ directory",
    )
    parser.add_argument(
        "--lang",
        default="ja",
        help="HTML lang attribute (default: ja)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress output messages",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose output",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    # Quiet mode overrides verbose
    verbose = args.verbose and not args.quiet

    try:
        # Default: delete intermediate files; --debug keeps them
        keep_html = args.debug
        output_path = convert_md_to_pdf(
            input_file=args.input,
            output_file=args.output,
            output_dir=args.output_dir,
            css_file=args.css,
            keep_html=keep_html,
            lang=args.lang,
            verbose=verbose,
        )

        if not args.quiet:
            print(f"PDF generated: {output_path}")

        return 0

    except FileNotFoundError as e:
        if not args.quiet:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        if not args.quiet:
            print(f"Error generating PDF: {e}", file=sys.stderr)
        if verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
