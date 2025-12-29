# gospelo-md2pdf

Convert Markdown to PDF with Japanese support and MermaidJS diagrams.

## Features

- **Japanese Text Support**: Full support for Japanese fonts (Noto Sans CJK JP, Hiragino Sans, Yu Gothic)
- **MermaidJS Diagrams**: Automatically renders Mermaid diagrams as PNG images via [Kroki API](https://kroki.io)
- **Custom CSS**: Use your own stylesheets or the built-in professional style
- **Markdown Extensions**: Tables, fenced code blocks, TOC, metadata, and more
- **Special HTML Classes**: Summary boxes, warnings, pros/cons sections, page breaks
- **Agent Skills**: Built-in support for AI coding assistants (Claude Code, VS Code Copilot)

## Installation

```bash
pip install gospelo-md2pdf
```

### System Dependencies

WeasyPrint requires system libraries. Install them first:

**macOS:**
```bash
brew install pango glib gdk-pixbuf libffi
```

**Ubuntu/Debian:**
```bash
sudo apt install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0
```

### Japanese Fonts (Recommended)

For Japanese text rendering:

**macOS:**
```bash
brew install font-noto-sans-cjk-jp
```

**Ubuntu/Debian:**
```bash
sudo apt install fonts-noto-cjk
```

### MermaidJS Support

Mermaid diagrams are rendered using the [Kroki API](https://kroki.io) (no local installation required). Supported Mermaid version depends on Kroki's implementation (currently Mermaid v11.x).

**For Web Claude**: Add `kroki.io` to allowed domains:
1. Settings (gear icon) → Capabilities
2. Find "Additional allowed domains"
3. Add `kroki.io`

## Quick Start

```bash
# Basic usage
gospelo-md2pdf report.md

# Specify output file
gospelo-md2pdf report.md output.pdf

# Specify output directory
gospelo-md2pdf report.md -o ./pdf

# Use custom CSS
gospelo-md2pdf report.md --css custom-style.css

# Keep intermediate files for debugging
gospelo-md2pdf report.md --debug
```

## Usage

```
gospelo-md2pdf <input.md> [output.pdf] [options]

Arguments:
  input.md              Input Markdown file
  output.pdf            Output PDF file (optional)

Options:
  -o, --output-dir DIR  Output directory (default: current directory)
  -c, --css FILE        Custom CSS file
  --debug               Keep intermediate files (HTML, mermaid) in tmp/ directory
  --lang LANG           HTML lang attribute (default: ja)
  -q, --quiet           Suppress output messages
  --verbose             Print verbose output
  -v, --version         Show version
  -h, --help            Show help
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MD2PDF_OUTPUT_DIR` | Output directory | Current directory |

Note: `--output-dir` option takes precedence over the environment variable.

## Markdown Features

### Basic Syntax

```markdown
# Heading 1
## Heading 2
### Heading 3

Paragraph with **bold** and *italic* text.

- Bullet list
- Another item
  - Nested item

1. Numbered list
2. Another item

> Blockquote

`inline code`

[Link](https://example.com)
```

### Tables

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| A        | B        | C        |
| D        | E        | F        |
```

### Code Blocks

````markdown
```python
def hello():
    print("Hello, World!")
```
````

### MermaidJS Diagrams

````markdown
```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[Result A]
    C -->|No| E[Result B]
```
````

Supported diagram types:
- Flowcharts (`graph TD`, `graph LR`)
- Sequence diagrams (`sequenceDiagram`)
- Class diagrams (`classDiagram`)
- State diagrams (`stateDiagram-v2`)
- ER diagrams (`erDiagram`)
- And all other Mermaid diagram types

Note: Tall diagrams are automatically scaled to fit within a single page (max-height: 700px) while preserving aspect ratio.

## Special HTML Classes

Use these HTML classes in your Markdown for special styling:

### Summary Box (Green)

```html
<div class="summary">
Important summary points here.
</div>
```

### Warning Box (Orange)

```html
<div class="warning">
Warning message here.
</div>
```

### Info Box (Blue)

```html
<div class="info">
Additional information here.
</div>
```

### Pros/Cons

```html
<div class="pros">
Pros: High scalability
</div>

<div class="cons">
Cons: Initial cost
</div>
```

### Disclaimer

```html
<div class="disclaimer">
This report is for informational purposes only.
</div>
```

### Page Break

```html
<div class="page-break"></div>
```

## Python API

```python
from gospelo_md2pdf import convert_md_to_pdf

# Basic usage
convert_md_to_pdf("report.md")

# With options
convert_md_to_pdf(
    input_file="report.md",
    output_file="output.pdf",
    output_dir="./pdf",
    css_file="custom.css",
    keep_html=True,
    lang="ja",
    verbose=True
)
```

## Troubleshooting

### Japanese text not rendering

Check if Japanese fonts are installed:

```bash
fc-list :lang=ja | head -5
```

### WeasyPrint library errors on macOS

Set the library path:

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

Add to `~/.zshrc` for persistence:

```bash
echo 'export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH' >> ~/.zshrc
source ~/.zshrc
```

### Mermaid diagrams not rendering

1. Verify network connectivity to `kroki.io`
2. For Web Claude: Add `kroki.io` to allowed domains (Settings → Capabilities → Additional allowed domains)
3. Check error messages for "Cannot connect to Kroki"

## Requirements

- Python >= 3.10
- weasyprint >= 60.0
- markdown >= 3.5.0
- System: pango, glib, gdk-pixbuf (see Installation)
- Network: Access to kroki.io (for Mermaid diagrams)

## Dependencies and Acknowledgements

This project uses the following open-source libraries. Full license texts are included in the [LICENSE](https://github.com/gorosun/gospelo-md2pdf/blob/main/LICENSE) file.

| Library | License | Description |
|---------|---------|-------------|
| [WeasyPrint](https://weasyprint.org/) | BSD 3-Clause | HTML/CSS to PDF converter |
| [Python-Markdown](https://python-markdown.github.io/) | BSD 3-Clause | Markdown to HTML converter |
| [Kroki](https://kroki.io) | MIT | Diagram rendering API |

### System Libraries (Dynamically Linked)

| Library | License | Description |
|---------|---------|-------------|
| [Pango](https://pango.gnome.org/) | LGPL 2.0+ | Text rendering |
| [GLib](https://docs.gtk.org/glib/) | LGPL 2.1+ | Core utilities |
| [GDK-Pixbuf](https://docs.gtk.org/gdk-pixbuf/) | LGPL 2.1+ | Image loading |

Note: System libraries are dynamically linked and not bundled with this package.

### Fonts (Recommended)

| Font | License | Description |
|------|---------|-------------|
| [Noto Sans CJK JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP) | OFL 1.1 | Japanese font by Google |

Note: Fonts are not bundled with this package. Users install them separately.

## License

MIT License - see [LICENSE](https://github.com/gorosun/gospelo-md2pdf/blob/main/LICENSE) for details.

## Author

NoStudio LLC (goro-hayakawa@no-studio.net)

## Documentation

- [日本語ドキュメント (Japanese)](https://github.com/gorosun/gospelo-md2pdf/blob/main/docs/README_jp.md)
- [Agent Skills Quick Start](https://github.com/gorosun/gospelo-md2pdf/blob/main/docs/AGENT_SKILLS.md)
- [CSS Template Guide](https://github.com/gorosun/gospelo-md2pdf/blob/main/docs/CSS_TEMPLATE_GUIDE.md)
- [Changelog](https://github.com/gorosun/gospelo-md2pdf/blob/main/docs/CHANGELOG.md)

## Links

- [GitHub Repository](https://github.com/gorosun/gospelo-md2pdf)
- [Issue Tracker](https://github.com/gorosun/gospelo-md2pdf/issues)
- [PyPI Package](https://pypi.org/project/gospelo-md2pdf/)
