"""Markdown to PDF Converter with Japanese support and MermaidJS diagrams.

Copyright (c) 2025 NoStudio LLC
Licensed under the MIT License. See LICENSE file for details.

This software uses WeasyPrint (BSD 3-Clause) and Python-Markdown (BSD 3-Clause).
See LICENSE file for third-party license information.
"""

__version__ = "1.1.2"

from .converter import convert_md_to_pdf, convert_md_to_html, convert_html_to_pdf

__all__ = ["convert_md_to_pdf", "convert_md_to_html", "convert_html_to_pdf", "__version__"]
