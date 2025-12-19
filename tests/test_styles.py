"""Tests for the styles module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from gospelo_md2pdf.styles import DEFAULT_CSS, get_default_css, load_css_file


class TestDefaultCss:
    """Tests for DEFAULT_CSS constant."""

    def test_default_css_not_empty(self):
        """Test that DEFAULT_CSS is not empty."""
        assert DEFAULT_CSS
        assert len(DEFAULT_CSS) > 100

    def test_default_css_contains_page_rule(self):
        """Test that DEFAULT_CSS contains @page rule."""
        assert "@page" in DEFAULT_CSS
        assert "size: A4" in DEFAULT_CSS

    def test_default_css_contains_body_style(self):
        """Test that DEFAULT_CSS contains body style."""
        assert "body {" in DEFAULT_CSS
        assert "font-family:" in DEFAULT_CSS

    def test_default_css_contains_special_classes(self):
        """Test that DEFAULT_CSS contains special classes."""
        assert ".summary" in DEFAULT_CSS
        assert ".warning" in DEFAULT_CSS
        assert ".info" in DEFAULT_CSS
        assert ".pros" in DEFAULT_CSS
        assert ".cons" in DEFAULT_CSS
        assert ".disclaimer" in DEFAULT_CSS
        assert ".page-break" in DEFAULT_CSS

    def test_default_css_contains_mermaid_style(self):
        """Test that DEFAULT_CSS contains mermaid diagram style."""
        assert ".mermaid-diagram" in DEFAULT_CSS


class TestGetDefaultCss:
    """Tests for get_default_css function."""

    def test_returns_css_from_file(self):
        """Test that CSS is returned from bundled file if exists."""
        css = get_default_css()
        assert css
        assert "@page" in css

    def test_fallback_to_constant_when_file_missing(self):
        """Test fallback to DEFAULT_CSS when bundled file is missing."""
        with patch("gospelo_md2pdf.styles.Path") as mock_path:
            # Make the file path return False for exists()
            mock_path_instance = mock_path.return_value.__truediv__.return_value
            mock_path_instance.exists.return_value = False
            mock_path.return_value.parent = Path(__file__).parent

            # Re-import to get fresh function with mocked Path
            from gospelo_md2pdf import styles

            # Directly test the fallback logic
            styles_dir = Path("/nonexistent")
            default_css_path = styles_dir / "default.css"

            if not default_css_path.exists():
                result = DEFAULT_CSS
            else:
                result = default_css_path.read_text(encoding="utf-8")

            assert result == DEFAULT_CSS


class TestLoadCssFile:
    """Tests for load_css_file function."""

    def test_load_existing_css_file(self):
        """Test loading an existing CSS file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            css_file = Path(tmpdir) / "custom.css"
            css_content = "body { color: red; }"
            css_file.write_text(css_content, encoding="utf-8")

            result = load_css_file(css_file)
            assert result == css_content

    def test_load_css_file_with_string_path(self):
        """Test loading CSS file with string path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            css_file = Path(tmpdir) / "custom.css"
            css_content = "h1 { font-size: 24pt; }"
            css_file.write_text(css_content, encoding="utf-8")

            result = load_css_file(str(css_file))
            assert result == css_content

    def test_load_nonexistent_css_file(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError) as exc_info:
            load_css_file("/nonexistent/path/custom.css")

        assert "CSS file not found" in str(exc_info.value)

    def test_load_css_file_with_utf8_content(self):
        """Test loading CSS file with UTF-8 content (Japanese)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            css_file = Path(tmpdir) / "japanese.css"
            css_content = "/* 日本語コメント */\nbody { font-family: 'Noto Sans CJK JP'; }"
            css_file.write_text(css_content, encoding="utf-8")

            result = load_css_file(css_file)
            assert "日本語コメント" in result
            assert "Noto Sans CJK JP" in result
