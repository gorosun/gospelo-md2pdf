# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-19

### Added

- Initial release
- Markdown to PDF conversion with WeasyPrint
- Japanese font support (Noto Sans CJK JP, Hiragino Sans, Yu Gothic)
- MermaidJS diagram support (PNG output via mermaid-cli)
- Custom CSS support
- Built-in professional PDF styles
- Special HTML classes: summary, warning, info, pros, cons, disclaimer, page-break
- CLI with multiple options:
  - `--output-dir`: Specify output directory
  - `--css`: Use custom CSS file
  - `--no-html`: Delete intermediate HTML file
  - `--lang`: Set HTML lang attribute
  - `--quiet`: Suppress output
  - `--verbose`: Verbose output
- Python API for programmatic usage
- Environment variable support (`MD2PDF_OUTPUT_DIR`)
