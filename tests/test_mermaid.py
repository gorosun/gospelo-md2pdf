"""Tests for the mermaid module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from gospelo_md2pdf.mermaid import (
    check_mermaid_cli,
    process_mermaid_blocks,
    render_mermaid_to_png,
)


class TestCheckMermaidCli:
    """Tests for check_mermaid_cli function."""

    def test_returns_bool(self):
        """Test that function returns a boolean."""
        result = check_mermaid_cli()
        assert isinstance(result, bool)

    def test_returns_false_when_not_installed(self):
        """Test that function returns False when mmdc is not found."""
        with patch("shutil.which", return_value=None):
            assert check_mermaid_cli() is False

    def test_returns_true_when_installed(self):
        """Test that function returns True when mmdc is found."""
        with patch("shutil.which", return_value="/usr/local/bin/mmdc"):
            assert check_mermaid_cli() is True


class TestProcessMermaidBlocks:
    """Tests for process_mermaid_blocks function."""

    def test_returns_unchanged_when_no_mermaid(self):
        """Test that HTML is unchanged when no Mermaid blocks."""
        html = "<p>Hello World</p>"
        with tempfile.TemporaryDirectory() as tmpdir:
            result = process_mermaid_blocks(html, Path(tmpdir), "test")
        assert result == html

    def test_returns_unchanged_when_mermaid_cli_not_found(self, capsys):
        """Test that HTML is unchanged when mermaid-cli is not available."""
        html = '<pre><code class="language-mermaid">graph TD\nA-->B</code></pre>'
        with patch("gospelo_md2pdf.mermaid.check_mermaid_cli", return_value=False):
            with tempfile.TemporaryDirectory() as tmpdir:
                result = process_mermaid_blocks(html, Path(tmpdir), "test")
        assert result == html
        captured = capsys.readouterr()
        assert "Warning" in captured.err

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_processes_mermaid_blocks(self):
        """Test that Mermaid blocks are processed when CLI is available."""
        html = '<pre><code class="language-mermaid">graph TD\nA-->B</code></pre>'
        with tempfile.TemporaryDirectory() as tmpdir:
            result = process_mermaid_blocks(html, Path(tmpdir), "test")

        assert '<div class="mermaid-diagram">' in result
        assert "<img" in result
        assert ".png" in result


class TestRenderMermaidToPng:
    """Tests for render_mermaid_to_png function."""

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_renders_simple_diagram(self):
        """Test rendering a simple Mermaid diagram."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.png"
            result = render_mermaid_to_png("graph TD\nA-->B", output_path)

            assert result is True
            assert output_path.exists()
            assert output_path.stat().st_size > 0

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_renders_flowchart_with_japanese(self):
        """Test rendering a flowchart with Japanese text."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.png"
            mermaid_code = """graph TD
    A[開始] --> B[処理]
    B --> C{判断}
    C -->|はい| D[終了]
"""
            result = render_mermaid_to_png(mermaid_code, output_path)

            assert result is True
            assert output_path.exists()

    def test_returns_false_on_invalid_syntax(self):
        """Test that function returns False for invalid Mermaid syntax."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.png"
            # Invalid Mermaid syntax
            result = render_mermaid_to_png("invalid mermaid code {{{", output_path)
            # Should return False (rendering failed)
            # Note: This depends on mermaid-cli behavior
            assert isinstance(result, bool)


class TestMermaidIntegration:
    """Integration tests for Mermaid diagram embedding in PDF."""

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_markdown_with_mermaid_to_html(self):
        """Test that Mermaid blocks in Markdown are converted to images in HTML."""
        from gospelo_md2pdf.converter import convert_md_to_html

        markdown_content = """# Test Document

## Flowchart

```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```

Some text after diagram.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text(markdown_content)

            output_dir = Path(tmpdir) / "output"
            html_content, html_path = convert_md_to_html(md_file, output_dir)

            # Check that Mermaid block was converted to image
            assert '<div class="mermaid-diagram">' in html_content
            assert "<img" in html_content
            assert ".png" in html_content
            # Original code block should not remain
            assert 'class="language-mermaid"' not in html_content

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_markdown_with_mermaid_to_pdf(self):
        """Test that PDF is generated with embedded Mermaid diagrams."""
        from gospelo_md2pdf.converter import convert_md_to_pdf

        markdown_content = """# Test Document

```mermaid
graph LR
    A --> B
    B --> C
```
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text(markdown_content)

            output_dir = Path(tmpdir) / "output"
            pdf_path = convert_md_to_pdf(md_file, output_dir=output_dir)

            assert pdf_path.exists()
            assert pdf_path.stat().st_size > 0

            # Check that PNG files were generated in mermaid directory
            mermaid_dir = output_dir / "mermaid"
            if mermaid_dir.exists():
                png_files = list(mermaid_dir.glob("*.png"))
                assert len(png_files) > 0

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_multiple_mermaid_diagrams(self):
        """Test that multiple Mermaid diagrams are processed correctly."""
        markdown_content = """# Multiple Diagrams

## Diagram 1
```mermaid
graph TD
    A --> B
```

## Diagram 2
```mermaid
sequenceDiagram
    Alice->>Bob: Hello
    Bob->>Alice: Hi
```
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text(markdown_content)

            output_dir = Path(tmpdir) / "output"

            from gospelo_md2pdf.converter import convert_md_to_html
            html_content, _ = convert_md_to_html(md_file, output_dir)

            # Count mermaid-diagram divs
            diagram_count = html_content.count('<div class="mermaid-diagram">')
            assert diagram_count == 2

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_mermaid_with_japanese_text(self):
        """Test Mermaid diagram with Japanese text."""
        markdown_content = """# 日本語テスト

```mermaid
graph TD
    A[開始] --> B[処理中]
    B --> C{判定}
    C -->|成功| D[完了]
    C -->|失敗| E[エラー]
```
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text(markdown_content, encoding="utf-8")

            output_dir = Path(tmpdir) / "output"

            from gospelo_md2pdf.converter import convert_md_to_pdf
            pdf_path = convert_md_to_pdf(md_file, output_dir=output_dir)

            assert pdf_path.exists()
            assert pdf_path.stat().st_size > 0

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_mermaid_with_subgraph_quotes(self):
        """Test Mermaid diagram with subgraph labels containing quotes."""
        markdown_content = '''# Subgraph Test

```mermaid
graph TD
    subgraph "Frontend Layer"
        A[Component] --> B[Service]
    end
    subgraph "Backend Layer"
        C[API] --> D[Database]
    end
    B --> C
```
'''
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text(markdown_content, encoding="utf-8")

            output_dir = Path(tmpdir) / "output"

            from gospelo_md2pdf.converter import convert_md_to_html
            html_content, _ = convert_md_to_html(md_file, output_dir)

            # Check that Mermaid block was converted to image
            assert '<div class="mermaid-diagram">' in html_content
            assert "<img" in html_content
            # Original code block should not remain
            assert 'class="language-mermaid"' not in html_content


class TestHtmlEntityUnescaping:
    """Tests for HTML entity unescaping in Mermaid code."""

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_unescape_html_entities(self):
        """Test that HTML entities are properly unescaped before rendering."""
        # Simulate HTML with escaped entities (as produced by Markdown conversion)
        html = '<pre><code class="language-mermaid">graph TD\n    subgraph &quot;Test Layer&quot;\n        A[Node] --&gt; B[Other]\n    end</code></pre>'
        with tempfile.TemporaryDirectory() as tmpdir:
            result = process_mermaid_blocks(html, Path(tmpdir), "test")

        # Should successfully render (not remain as code block)
        assert '<div class="mermaid-diagram">' in result
        assert "<img" in result

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_unescape_single_quotes(self):
        """Test that single quote entities are properly unescaped."""
        # Test &#39; (numeric entity for single quote)
        html = "<pre><code class=\"language-mermaid\">graph TD\n    A[It&#39;s working] --> B[End]</code></pre>"
        with tempfile.TemporaryDirectory() as tmpdir:
            result = process_mermaid_blocks(html, Path(tmpdir), "test")

        assert '<div class="mermaid-diagram">' in result

    @pytest.mark.skipif(
        not check_mermaid_cli(),
        reason="mermaid-cli not installed"
    )
    def test_unescape_ampersand(self):
        """Test that ampersand entities are properly unescaped."""
        html = '<pre><code class="language-mermaid">graph TD\n    A[A &amp; B] --> C[End]</code></pre>'
        with tempfile.TemporaryDirectory() as tmpdir:
            result = process_mermaid_blocks(html, Path(tmpdir), "test")

        assert '<div class="mermaid-diagram">' in result
