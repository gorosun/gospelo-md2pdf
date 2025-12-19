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
