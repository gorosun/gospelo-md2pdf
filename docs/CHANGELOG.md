# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-12-30

### Changed

- Standardized skill location to `.github/skills/` (removed `.claude/skills/`)
- Updated SKILL.md: replaced deprecated `--no-html` option with `--debug`
- Added `marketplace.json` for SkillsMP integration

### Added

- Official documentation links in AGENT_SKILLS.md and AGENT_SKILLS_jp.md
  - Agent Skills Overview (platform.claude.com)
  - Introducing Agent Skills (anthropic.com/news)
  - anthropics/skills Repository

## [1.2.0] - 2025-12-29

### Changed

- **Breaking**: Switched Mermaid rendering from mermaid-cli to Kroki API
  - No longer requires `npm install -g @mermaid-js/mermaid-cli`
  - Uses [Kroki.io](https://kroki.io) free service for rendering
  - For Web Claude: Add `kroki.io` to allowed domains in Settings → Capabilities
  - POST method used to avoid URL length limitations

### Added

- Auto-scaling for tall Mermaid diagrams to fit within a single page
  - `max-height: 700px` (~85% of A4 page height)
  - `object-fit: contain` preserves aspect ratio
  - `page-break-inside: avoid` prevents diagram splitting

### Removed

- Dependency on mermaid-cli (npm package)

## [1.1.1] - 2025-12-26

### Changed

- Replaced `--no-html` option with `--debug` option
  - `--debug` keeps intermediate files (HTML, mermaid) in tmp/ directory for debugging
- Updated documentation with `--debug` option usage

## [1.1.0] - 2025-12-24

### Added

- Agent Skills support for AI coding assistants (Claude Code, VS Code Copilot)
  - Added `.claude/skills/gospelo-md2pdf/SKILL.md` for Claude Code
  - Added `.github/skills/gospelo-md2pdf/SKILL.md` for VS Code Copilot
  - Added Agent Skills documentation (`docs/AGENT_SKILLS.md`, `docs/AGENT_SKILLS_jp.md`)

## [1.0.1] - 2025-12-19

### Fixed

- Fixed HTML entity unescaping in Mermaid code blocks
  - Added support for `&quot;` (double quote) unescaping
  - Added support for `&#39;` and `&apos;` (single quote) unescaping
  - Fixed `&amp;` processing order to prevent double-unescaping
  - Resolves parse errors with `subgraph "Label"` syntax

### Added

- New test cases for HTML entity unescaping (4 tests)
  - `test_mermaid_with_subgraph_quotes`
  - `test_unescape_html_entities`
  - `test_unescape_single_quotes`
  - `test_unescape_ampersand`

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
