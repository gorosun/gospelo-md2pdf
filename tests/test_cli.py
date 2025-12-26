"""Tests for the CLI module."""

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from gospelo_md2pdf.cli import main


class TestCLI:
    """Tests for CLI functionality."""

    def test_help_option(self, capsys):
        """Test --help option."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["gospelo-md2pdf", "--help"]):
                main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Convert Markdown to PDF" in captured.out

    def test_version_option(self, capsys):
        """Test --version option."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["gospelo-md2pdf", "--version"]):
                main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "gospelo-md2pdf" in captured.out

    def test_missing_input_file(self, capsys):
        """Test error when input file is missing."""
        with patch.object(sys, "argv", ["gospelo-md2pdf", "/nonexistent/file.md"]):
            result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_basic_conversion(self, capsys):
        """Test basic file conversion."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Hello World")

            with patch.object(
                sys, "argv", ["gospelo-md2pdf", str(md_file), "-o", tmpdir]
            ):
                result = main()

            assert result == 0
            pdf_file = Path(tmpdir) / "test.pdf"
            assert pdf_file.exists()
            captured = capsys.readouterr()
            assert "PDF generated" in captured.out

    def test_quiet_mode(self, capsys):
        """Test quiet mode suppresses output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Hello World")

            with patch.object(
                sys, "argv", ["gospelo-md2pdf", str(md_file), "-o", tmpdir, "--quiet"]
            ):
                result = main()

            assert result == 0
            captured = capsys.readouterr()
            assert captured.out == ""

    def test_default_removes_intermediate_files(self):
        """Test default behavior removes intermediate files (tmp/ directory)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Hello World")

            with patch.object(
                sys, "argv", ["gospelo-md2pdf", str(md_file), "-o", tmpdir]
            ):
                main()

            # tmp/ directory should not exist (cleaned up by default)
            tmp_dir = Path(tmpdir) / "tmp"
            assert not tmp_dir.exists()

    def test_debug_option_keeps_intermediate_files(self):
        """Test --debug keeps intermediate files in tmp/ directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text("# Hello World")

            with patch.object(
                sys, "argv", ["gospelo-md2pdf", str(md_file), "-o", tmpdir, "--debug"]
            ):
                main()

            # tmp/ directory should exist with HTML file
            tmp_dir = Path(tmpdir) / "tmp"
            assert tmp_dir.exists()
            html_file = tmp_dir / "test.html"
            assert html_file.exists()
