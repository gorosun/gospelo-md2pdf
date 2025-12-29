# Agent Skills Quick Start

gospelo-md2pdf supports [Agent Skills](https://agentskills.io/specification), an open standard for AI agent capabilities.

## What is Agent Skills?

Agent Skills is an open standard introduced by Anthropic that allows AI agents to discover and use specialized capabilities dynamically. gospelo-md2pdf includes a built-in skill that enables AI coding assistants to convert Markdown to PDF automatically.

## Supported Platforms

| Platform | Skill Location | Status |
|----------|---------------|--------|
| Claude Code | `.github/skills/gospelo-md2pdf/` | Supported |
| VS Code Copilot | `.github/skills/gospelo-md2pdf/` | Supported |

Note: `.github/skills/` is the standard location for Agent Skills. Both Claude Code and VS Code Copilot support this location.

## Quick Start

### 1. Install gospelo-md2pdf

```bash
pip install gospelo-md2pdf
```

### 2. Copy the Skill to Your Project

Copy the skill folder to your project:

```bash
cp -r path/to/gospelo-md2pdf/.github/skills/gospelo-md2pdf .github/skills/
```

Or manually create the skill file (see [Skill File](#skill-file) below).

### 3. Use with AI Assistant

Simply ask your AI assistant to convert a Markdown file to PDF:

```
"Convert README.md to PDF"
"Generate a PDF from docs/guide.md"
"Export this document as PDF"
```

The AI assistant will automatically detect the skill and use gospelo-md2pdf.

## Skill File

### Location

`.github/skills/gospelo-md2pdf/SKILL.md`

### Content

```yaml
---
name: gospelo-md2pdf
description: Convert Markdown files to PDF with Japanese support and MermaidJS diagrams using gospelo-md2pdf. Use when asked to create PDF, generate PDF, export to PDF, or convert markdown to PDF.
allowed-tools: Read, Bash(gospelo-md2pdf:*)
---

# PDF Generation Skill

...
```

See the full skill file at [.github/skills/gospelo-md2pdf/SKILL.md](https://github.com/gorosun/gospelo-md2pdf/blob/main/.github/skills/gospelo-md2pdf/SKILL.md).

## Personal Skills (Global)

To use the skill across all projects, install it to your personal skills directory:

```bash
mkdir -p ~/.claude/skills/gospelo-md2pdf
cp .github/skills/gospelo-md2pdf/SKILL.md ~/.claude/skills/gospelo-md2pdf/
```

Note: Personal skills are stored in `~/.claude/skills/` for Claude Code.

## Troubleshooting

### macOS Library Errors

If WeasyPrint library errors occur, set the library path:

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

Add to `~/.zshrc` for persistence.

### Skill Not Detected

1. Verify the skill file exists in the correct location
2. Check the file name is exactly `SKILL.md`
3. Ensure the frontmatter (YAML between `---`) is valid

## Related Links

- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) - Official Claude platform documentation
- [Introducing Agent Skills](https://www.anthropic.com/news/skills) - Anthropic announcement
- [anthropics/skills Repository](https://github.com/anthropics/skills) - Official skills repository (uses `.github/skills/` standard)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills)
- [gospelo-md2pdf GitHub](https://github.com/gorosun/gospelo-md2pdf)
