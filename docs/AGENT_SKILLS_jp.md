# Agent Skills クイックスタート

gospelo-md2pdfは、AIエージェント向けのオープンスタンダードである[Agent Skills](https://agentskills.io/specification)に対応しています。

## Agent Skillsとは？

Agent Skillsは、Anthropicが提唱したオープンスタンダードで、AIエージェントが専門的な能力を動的に発見・使用できるようにするものです。gospelo-md2pdfには、AIコーディングアシスタントがMarkdownをPDFに自動変換できるスキルが組み込まれています。

## 対応プラットフォーム

| プラットフォーム | スキルの場所 | 対応状況 |
|----------------|------------|---------|
| Claude Code | `.claude/skills/gospelo-md2pdf/` | 対応済み |
| VS Code Copilot (Insiders) | `.github/skills/gospelo-md2pdf/` | 対応済み |
| VS Code Copilot (Stable) | `.claude/skills/gospelo-md2pdf/` | 対応予定（2026年1月〜） |

## クイックスタート

### 1. gospelo-md2pdfをインストール

```bash
pip install gospelo-md2pdf
```

### 2. スキルをプロジェクトにコピー

スキルフォルダをプロジェクトにコピーします：

```bash
# Claude Code用
cp -r path/to/gospelo-md2pdf/.claude/skills/gospelo-md2pdf .claude/skills/

# VS Code Copilot (Insiders)用
cp -r path/to/gospelo-md2pdf/.github/skills/gospelo-md2pdf .github/skills/
```

または、スキルファイルを手動で作成することもできます（下記[スキルファイル](#スキルファイル)参照）。

### 3. AIアシスタントで使用

AIアシスタントにMarkdownファイルのPDF変換を依頼するだけです：

```
「README.mdをPDFに変換して」
「docs/guide.mdからPDFを生成して」
「このドキュメントをPDFで出力して」
```

AIアシスタントが自動的にスキルを検出し、gospelo-md2pdfを使用します。

## スキルファイル

### 配置場所

- **Claude Code**: `.claude/skills/gospelo-md2pdf/SKILL.md`
- **VS Code Copilot**: `.github/skills/gospelo-md2pdf/SKILL.md`

### 内容

```yaml
---
name: gospelo-md2pdf
description: Convert Markdown files to PDF with Japanese support and MermaidJS diagrams using gospelo-md2pdf. Use when asked to create PDF, generate PDF, export to PDF, or convert markdown to PDF.
allowed-tools: Read, Bash(gospelo-md2pdf:*)
---

# PDF Generation Skill

...
```

完全なスキルファイルは [.claude/skills/gospelo-md2pdf/SKILL.md](https://github.com/gorosun/gospelo-md2pdf/blob/main/.claude/skills/gospelo-md2pdf/SKILL.md) を参照してください。

## パーソナルスキル（グローバル）

すべてのプロジェクトでスキルを使用するには、パーソナルスキルディレクトリにインストールします：

```bash
# Claude Code
mkdir -p ~/.claude/skills/gospelo-md2pdf
cp .claude/skills/gospelo-md2pdf/SKILL.md ~/.claude/skills/gospelo-md2pdf/
```

## トラブルシューティング

### macOSでライブラリエラーが発生する

WeasyPrintのライブラリエラーが発生した場合、ライブラリパスを設定してください：

```bash
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

永続化するには `~/.zshrc` に追加してください。

### スキルが検出されない

1. スキルファイルが正しい場所に存在するか確認
2. ファイル名が正確に `SKILL.md` であることを確認
3. フロントマター（`---` で囲まれたYAML部分）が正しい形式か確認

## 関連リンク

- [Agent Skills 仕様](https://agentskills.io/specification)
- [Claude Code Skills ドキュメント](https://docs.anthropic.com/en/docs/claude-code/skills)
- [gospelo-md2pdf GitHub](https://github.com/gorosun/gospelo-md2pdf)
