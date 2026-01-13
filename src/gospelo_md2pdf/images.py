"""Image processing for embedding images as Base64 data URIs."""

from __future__ import annotations

import base64
import mimetypes
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _get_mime_type(path: str) -> str:
    """
    Get MIME type for an image file.

    Args:
        path: File path or URL

    Returns:
        MIME type string (e.g., "image/png")
    """
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type and mime_type.startswith("image/"):
        return mime_type
    # Default to PNG if unknown
    return "image/png"


def _load_local_image(path: Path) -> bytes | None:
    """
    Load image from local filesystem.

    Args:
        path: Path to image file

    Returns:
        Image bytes or None if file not found
    """
    try:
        return path.read_bytes()
    except (FileNotFoundError, PermissionError, OSError):
        return None


def _load_remote_image(url: str) -> bytes | None:
    """
    Load image from HTTP/HTTPS URL.

    Args:
        url: Image URL

    Returns:
        Image bytes or None if fetch failed
    """
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "gospelo-md2pdf/1.0"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data: bytes = response.read()
            return data
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
        return None


def _to_base64_data_uri(image_data: bytes, mime_type: str) -> str:
    """
    Convert image bytes to Base64 data URI.

    Args:
        image_data: Image bytes
        mime_type: MIME type string

    Returns:
        Data URI string (e.g., "data:image/png;base64,...")
    """
    encoded = base64.b64encode(image_data).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def process_image_paths(
    html_content: str, input_dir: Path, verbose: bool = False
) -> str:
    """
    Find img tags in HTML and embed images as Base64 data URIs.

    Handles:
    - Relative paths: ./images/photo.png (resolved from input_dir)
    - Absolute paths: /home/user/img.png
    - HTTP/HTTPS URLs: https://example.com/image.png (fetched and embedded)
    - data URIs: Already embedded, left unchanged

    Args:
        html_content: HTML content with img tags
        input_dir: Directory of the input Markdown file (for resolving relative paths)
        verbose: Whether to print verbose output

    Returns:
        HTML content with images embedded as Base64 data URIs
    """
    # Pattern to match img tags and capture src attribute
    img_pattern = re.compile(
        r'<img\s+([^>]*?)src=["\']([^"\']+)["\']([^>]*?)/?>', re.IGNORECASE
    )

    image_count = 0
    failed_count = 0

    def replace_image(match: re.Match[str]) -> str:
        nonlocal image_count, failed_count

        original: str = match.group(0)
        before_src: str = match.group(1)
        src: str = match.group(2)
        after_src: str = match.group(3)

        # Skip if already a data URI
        if src.startswith("data:"):
            return original

        # Determine if URL or local path
        if src.startswith(("http://", "https://")):
            # Remote URL
            image_data = _load_remote_image(src)
            if image_data is None:
                print(f"Warning: Failed to fetch image: {src}", file=sys.stderr)
                failed_count += 1
                return original
            mime_type = _get_mime_type(src)
        else:
            # Local path
            if src.startswith("/"):
                # Absolute path
                image_path = Path(src)
            else:
                # Relative path - resolve from input directory
                image_path = (input_dir / src).resolve()

            image_data = _load_local_image(image_path)
            if image_data is None:
                print(f"Warning: Image not found: {image_path}", file=sys.stderr)
                failed_count += 1
                return original
            mime_type = _get_mime_type(str(image_path))

        # Convert to Base64 data URI
        data_uri = _to_base64_data_uri(image_data, mime_type)
        image_count += 1

        if verbose:
            print(f"  Embedded image: {src}")

        return f'<img {before_src}src="{data_uri}"{after_src}/>'

    result = img_pattern.sub(replace_image, html_content)

    if verbose and (image_count > 0 or failed_count > 0):
        print(f"  Total images embedded: {image_count}")
        if failed_count > 0:
            print(f"  Failed to embed: {failed_count}")

    return result
