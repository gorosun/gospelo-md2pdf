"""Mermaid diagram processing using Kroki API."""

import base64
import hashlib
import re
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path

# Kroki API endpoint
KROKI_URL = "https://kroki.io/mermaid/png"


def _encode_mermaid_for_kroki(mermaid_code: str) -> str:
    """
    Encode Mermaid code for Kroki API using deflate + base64.

    Args:
        mermaid_code: Mermaid diagram code

    Returns:
        URL-safe base64 encoded string
    """
    # Normalize: strip leading/trailing whitespace
    normalized = mermaid_code.strip()

    # Compress with zlib (deflate)
    compressed = zlib.compress(normalized.encode("utf-8"), level=9)

    # Base64 encode (URL-safe)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
    return encoded


def render_mermaid_to_png(mermaid_code: str, output_path: Path, scale: int = 2) -> bool:
    """
    Render Mermaid code to PNG using Kroki API.

    Uses POST method to avoid URL length limitations.

    Args:
        mermaid_code: Mermaid diagram code
        output_path: Path to save the PNG file
        scale: Scale factor for output quality (not supported by Kroki, ignored)

    Returns:
        True if successful, False otherwise
    """
    try:
        # Normalize code
        normalized = mermaid_code.strip()

        # Use POST method to avoid URL length limitations
        request = urllib.request.Request(
            KROKI_URL,
            data=normalized.encode("utf-8"),
            headers={
                "User-Agent": "gospelo-md2pdf/1.0",
                "Content-Type": "text/plain",
            },
            method="POST",
        )

        # Fetch PNG from Kroki
        with urllib.request.urlopen(request, timeout=30) as response:
            png_data = response.read()

        # Save PNG file
        output_path.write_bytes(png_data)
        return True

    except urllib.error.HTTPError as e:
        print(f"Warning: Kroki API error (HTTP {e.code}): {e.reason}", file=sys.stderr)
        return False
    except urllib.error.URLError as e:
        print(
            f"Warning: Cannot connect to Kroki: {e.reason}",
            file=sys.stderr,
        )
        print(
            "  For Web Claude: Settings → Capabilities → Additional allowed domains → Add 'kroki.io'",
            file=sys.stderr,
        )
        return False
    except Exception as e:
        print(f"Warning: Mermaid rendering error: {e}", file=sys.stderr)
        return False


def process_mermaid_blocks(
    html_content: str, output_dir: Path, base_name: str, verbose: bool = False
) -> str:
    """
    Find and process Mermaid code blocks in HTML, replacing them with PNG images.

    Uses Kroki API for rendering. PNG format is used instead of SVG because
    SVG foreignObject (used by Mermaid flowcharts) is not fully supported by WeasyPrint.

    Args:
        html_content: HTML content with Mermaid code blocks
        output_dir: Directory to save PNG files
        base_name: Base name for PNG files
        verbose: Whether to print verbose output

    Returns:
        HTML content with Mermaid blocks replaced by img tags
    """
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
        import html

        mermaid_code = html.unescape(mermaid_code)

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
