"""Mermaid diagram processing using mermaid-cli."""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def check_mermaid_cli() -> bool:
    """
    Check if mermaid-cli (mmdc) is available.

    Returns:
        True if mmdc is available, False otherwise
    """
    return shutil.which("mmdc") is not None


def render_mermaid_to_png(mermaid_code: str, output_path: Path, scale: int = 2) -> bool:
    """
    Render Mermaid code to PNG using mermaid-cli.

    PNG format is more reliable for PDF embedding than SVG with foreignObject,
    which is not fully supported by WeasyPrint.

    Args:
        mermaid_code: Mermaid diagram code
        output_path: Path to save the PNG file
        scale: Scale factor for output quality (default: 2)

    Returns:
        True if successful, False otherwise
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".mmd", delete=False, encoding="utf-8"
        ) as f:
            f.write(mermaid_code)
            temp_input = f.name

        # Use PNG output with higher scale for quality
        result = subprocess.run(
            ["mmdc", "-i", temp_input, "-o", str(output_path), "-b", "white", "-s", str(scale)],
            capture_output=True,
            text=True,
        )

        os.unlink(temp_input)

        if result.returncode != 0:
            print(f"Warning: Mermaid rendering failed: {result.stderr}", file=sys.stderr)
            return False

        return True
    except Exception as e:
        print(f"Warning: Mermaid rendering error: {e}", file=sys.stderr)
        return False


def process_mermaid_blocks(
    html_content: str, output_dir: Path, base_name: str, verbose: bool = False
) -> str:
    """
    Find and process Mermaid code blocks in HTML, replacing them with PNG images.

    PNG format is used instead of SVG because SVG foreignObject (used by Mermaid flowcharts)
    is not fully supported by WeasyPrint.

    Args:
        html_content: HTML content with Mermaid code blocks
        output_dir: Directory to save PNG files
        base_name: Base name for PNG files
        verbose: Whether to print verbose output

    Returns:
        HTML content with Mermaid blocks replaced by img tags
    """
    if not check_mermaid_cli():
        print(
            "Warning: mermaid-cli (mmdc) not found. Mermaid diagrams will not be rendered.",
            file=sys.stderr,
        )
        print("Install with: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
        return html_content

    # Pattern to match Mermaid code blocks in HTML
    # Matches <pre><code class="language-mermaid">...</code></pre> or similar
    mermaid_pattern = re.compile(
        r'<pre><code class="(?:language-)?mermaid">(.*?)</code></pre>', re.DOTALL
    )

    mermaid_dir = output_dir / "mermaid"
    mermaid_dir.mkdir(parents=True, exist_ok=True)

    diagram_count = 0

    def replace_mermaid(match):
        nonlocal diagram_count
        mermaid_code = match.group(1)
        # Unescape HTML entities
        mermaid_code = (
            mermaid_code.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&#39;", "'")
            .replace("&apos;", "'")
            .replace("&amp;", "&")  # &amp; must be last to avoid double-unescaping
        )

        # Generate unique filename
        code_hash = hashlib.md5(mermaid_code.encode()).hexdigest()[:8]
        png_filename = f"{base_name}_mermaid_{code_hash}.png"
        png_path = mermaid_dir / png_filename

        if render_mermaid_to_png(mermaid_code, png_path):
            diagram_count += 1
            if verbose:
                print(f"  Rendered Mermaid diagram: {png_filename}")
            # Return img tag with absolute path for WeasyPrint
            # max-height: 85vh ensures tall diagrams fit within a page
            # object-fit: contain preserves aspect ratio while fitting
            return f'<div class="mermaid-diagram"><img src="file://{png_path.absolute()}" alt="Mermaid Diagram"/></div>'
        else:
            # If rendering fails, keep the code block
            return match.group(0)

    result = mermaid_pattern.sub(replace_mermaid, html_content)

    if verbose and diagram_count > 0:
        print(f"  Total Mermaid diagrams rendered: {diagram_count}")

    return result
