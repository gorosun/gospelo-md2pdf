"""Tests for the converter module."""

import os
import tempfile
from pathlib import Path

import pytest

from gospelo_md2pdf.converter import (
    convert_md_to_html,
    convert_md_to_pdf,
    get_output_dir,
)


class TestGetOutputDir:
    """Tests for get_output_dir function."""

    def test_explicit_output_dir(self):
        """Test that explicit output_dir parameter takes precedence."""
        result = get_output_dir("/custom/path")
        assert result == Path("/custom/path")

    def test_env_variable(self, monkeypatch):
        """Test that environment variable is used when no explicit dir."""
        monkeypatch.setenv("MD2PDF_OUTPUT_DIR", "/env/path")
        result = get_output_dir(None)
        assert result == Path("/env/path")

    def test_default_to_cwd(self, monkeypatch):
        """Test that current working directory is used as default."""
        monkeypatch.delenv("MD2PDF_OUTPUT_DIR", raising=False)
        result = get_output_dir(None)
        assert result == Path.cwd()


class TestConvertMdToHtml:
    """Tests for convert_md_to_html function."""

    def test_basic_conversion(self):
        """Test basic Markdown to HTML conversion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test markdown file
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Hello World\n\nThis is a test.")

            output_dir = Path(tmpdir) / "output"
            html_content, html_path = convert_md_to_html(md_file, output_dir)

            assert "<h1" in html_content and "Hello World</h1>" in html_content
            assert "<p>This is a test.</p>" in html_content
            assert html_path.exists()
            assert html_path.suffix == ".html"

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                convert_md_to_html("/nonexistent/file.md", Path(tmpdir))

    def test_table_conversion(self):
        """Test that tables are converted correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("| A | B |\n|---|---|\n| 1 | 2 |")

            output_dir = Path(tmpdir) / "output"
            html_content, _ = convert_md_to_html(md_file, output_dir)

            assert "<table>" in html_content
            assert "<th>" in html_content
            assert "<td>" in html_content

    def test_code_block_conversion(self):
        """Test that code blocks are converted correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("```python\nprint('hello')\n```")

            output_dir = Path(tmpdir) / "output"
            html_content, _ = convert_md_to_html(md_file, output_dir)

            assert "<code" in html_content
            assert "print" in html_content

    def test_custom_lang_attribute(self):
        """Test that lang attribute is set correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Test")

            output_dir = Path(tmpdir) / "output"
            html_content, _ = convert_md_to_html(md_file, output_dir, lang="en")

            assert 'lang="en"' in html_content


class TestConvertMdToPdf:
    """Tests for convert_md_to_pdf function."""

    def test_basic_pdf_generation(self):
        """Test basic PDF generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Hello World\n\nThis is a test.")

            output_dir = Path(tmpdir) / "output"
            pdf_path = convert_md_to_pdf(md_file, output_dir=output_dir)

            assert pdf_path.exists()
            assert pdf_path.suffix == ".pdf"
            assert pdf_path.stat().st_size > 0

    def test_html_file_kept_by_default(self):
        """Test that HTML file is kept in tmp/ by default."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Test")

            output_dir = Path(tmpdir) / "output"
            convert_md_to_pdf(md_file, output_dir=output_dir, keep_html=True)

            # HTML file should be in tmp/ subdirectory
            html_path = output_dir / "tmp" / "test.html"
            assert html_path.exists()

    def test_html_file_removed_when_requested(self):
        """Test that tmp/ directory is removed when keep_html=False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Test")

            output_dir = Path(tmpdir) / "output"
            convert_md_to_pdf(md_file, output_dir=output_dir, keep_html=False)

            # Entire tmp/ directory should be removed
            tmp_dir = output_dir / "tmp"
            assert not tmp_dir.exists()

    def test_custom_output_file(self):
        """Test custom output file name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Test")

            output_dir = Path(tmpdir) / "output"
            pdf_path = convert_md_to_pdf(
                md_file, output_file="custom.pdf", output_dir=output_dir
            )

            assert pdf_path.name == "custom.pdf"
            assert pdf_path.exists()
