---
name: gospelo-md2pdf
description: Convert Markdown files to PDF with Japanese support and MermaidJS diagrams using gospelo-md2pdf. Use when asked to create PDF, generate PDF, export to PDF, or convert markdown to PDF.
allowed-tools: Read, Bash(gospelo-md2pdf:*)
---

# PDF Generation Skill

MarkdownファイルをPDFに変換するスキルです。日本語テキストとMermaidJSダイアグラムをサポートしています。

## When to Use

Activate this skill when the user asks to:
- Convert markdown to PDF
- Generate a PDF document
- Export a report as PDF
- Create a PDF with diagrams

## Prerequisites (macOS)

If WeasyPrint library errors occur, set the library path:

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

## Instructions

1. 変換対象のMarkdownファイルを確認する
2. ユーザーが出力先を指定した場合は `-o` オプションで出力ディレクトリを指定する
3. gospelo-md2pdfコマンドを実行する（macOSでライブラリエラーが出る場合は環境変数を設定）

### Basic Usage

```bash
# 基本的な使い方（同じディレクトリにPDFを出力）
gospelo-md2pdf input.md

# 出力ファイル名を指定
gospelo-md2pdf input.md output.pdf

# 出力ディレクトリを指定
gospelo-md2pdf input.md -o ./pdf

# 中間HTMLファイルを削除
gospelo-md2pdf input.md --no-html

# カスタムCSSを使用
gospelo-md2pdf input.md --css custom.css
```

## Options

| Option | Description |
|--------|-------------|
| `-o, --output-dir DIR` | Output directory |
| `-c, --css FILE` | Custom CSS file |
| `--no-html` | Delete intermediate HTML file |
| `--lang LANG` | HTML lang attribute (default: ja) |
| `-q, --quiet` | Suppress output messages |
| `--verbose` | Print verbose output |

## Supported Features

- **Japanese Text**: Full support for Japanese fonts
- **MermaidJS Diagrams**: Flowcharts, sequence diagrams, class diagrams, etc.
- **Tables**: GitHub-flavored markdown tables
- **Code Blocks**: Syntax highlighted code blocks
- **Special HTML Classes**: summary, warning, info, pros, cons, disclaimer, page-break

## Examples

### Convert a simple markdown file
```bash
gospelo-md2pdf report.md
```

### Convert with custom output location
```bash
gospelo-md2pdf docs/guide.md -o ./output
```

### Convert multiple files
```bash
for f in docs/*.md; do gospelo-md2pdf "$f" -o ./pdf; done
```
