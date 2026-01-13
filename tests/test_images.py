"""Tests for the images module."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from gospelo_md2pdf.images import (
    _get_mime_type,
    _load_local_image,
    _load_remote_image,
    _to_base64_data_uri,
    process_image_paths,
)


class TestGetMimeType:
    """Tests for _get_mime_type function."""

    def test_returns_png_for_png_file(self):
        """Test that PNG files return image/png."""
        assert _get_mime_type("test.png") == "image/png"
        assert _get_mime_type("/path/to/image.png") == "image/png"

    def test_returns_jpeg_for_jpg_file(self):
        """Test that JPG files return image/jpeg."""
        assert _get_mime_type("test.jpg") == "image/jpeg"
        assert _get_mime_type("test.jpeg") == "image/jpeg"

    def test_returns_gif_for_gif_file(self):
        """Test that GIF files return image/gif."""
        assert _get_mime_type("test.gif") == "image/gif"

    def test_returns_webp_for_webp_file(self):
        """Test that WebP files return image/webp."""
        assert _get_mime_type("test.webp") == "image/webp"

    def test_returns_svg_for_svg_file(self):
        """Test that SVG files return image/svg+xml."""
        assert _get_mime_type("test.svg") == "image/svg+xml"

    def test_returns_default_for_unknown(self):
        """Test that unknown extensions return image/png as default."""
        assert _get_mime_type("test.unknown") == "image/png"
        assert _get_mime_type("noextension") == "image/png"

    def test_handles_urls(self):
        """Test that URLs are handled correctly."""
        assert _get_mime_type("https://example.com/image.png") == "image/png"
        assert _get_mime_type("https://example.com/photo.jpg?size=large") == "image/jpeg"


class TestLoadLocalImage:
    """Tests for _load_local_image function."""

    def test_loads_existing_file(self):
        """Test loading an existing image file."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            test_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
            f.write(test_data)
            f.flush()

            result = _load_local_image(Path(f.name))
            assert result == test_data

    def test_returns_none_for_missing_file(self):
        """Test that missing files return None."""
        result = _load_local_image(Path("/nonexistent/image.png"))
        assert result is None

    def test_returns_none_for_permission_error(self):
        """Test that permission errors return None."""
        with patch.object(Path, "read_bytes", side_effect=PermissionError):
            result = _load_local_image(Path("/some/file.png"))
            assert result is None


class TestLoadRemoteImage:
    """Tests for _load_remote_image function."""

    def test_fetches_remote_image(self):
        """Test fetching a remote image."""
        mock_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100

        mock_response = MagicMock()
        mock_response.read.return_value = mock_data
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            result = _load_remote_image("https://example.com/image.png")
            assert result == mock_data

    def test_returns_none_for_url_error(self):
        """Test that URL errors return None."""
        import urllib.error

        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test")):
            result = _load_remote_image("https://example.com/image.png")
            assert result is None

    def test_returns_none_for_http_error(self):
        """Test that HTTP errors return None."""
        import urllib.error

        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
            "https://example.com/image.png", 404, "Not Found", {}, None
        )):
            result = _load_remote_image("https://example.com/image.png")
            assert result is None

    def test_returns_none_for_timeout(self):
        """Test that timeouts return None."""
        with patch("urllib.request.urlopen", side_effect=TimeoutError):
            result = _load_remote_image("https://example.com/image.png")
            assert result is None


class TestToBase64DataUri:
    """Tests for _to_base64_data_uri function."""

    def test_creates_valid_data_uri(self):
        """Test creating a valid Base64 data URI."""
        data = b"test data"
        result = _to_base64_data_uri(data, "image/png")

        assert result.startswith("data:image/png;base64,")
        # Verify it's valid base64
        import base64
        encoded_part = result.split(",")[1]
        decoded = base64.b64decode(encoded_part)
        assert decoded == data

    def test_handles_different_mime_types(self):
        """Test different MIME types in data URI."""
        data = b"test"

        assert _to_base64_data_uri(data, "image/jpeg").startswith("data:image/jpeg;base64,")
        assert _to_base64_data_uri(data, "image/gif").startswith("data:image/gif;base64,")
        assert _to_base64_data_uri(data, "image/webp").startswith("data:image/webp;base64,")


class TestProcessImagePaths:
    """Tests for process_image_paths function."""

    def test_returns_unchanged_when_no_images(self):
        """Test that HTML without images is unchanged."""
        html = "<p>Hello World</p>"
        result = process_image_paths(html, Path("/tmp"))
        assert result == html

    def test_skips_data_uri_images(self):
        """Test that existing data URIs are not modified."""
        html = '<img src="data:image/png;base64,ABC123"/>'
        result = process_image_paths(html, Path("/tmp"))
        assert result == html

    def test_embeds_local_image(self):
        """Test embedding a local image."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test image
            image_path = Path(tmpdir) / "test.png"
            image_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 50
            image_path.write_bytes(image_data)

            html = '<img src="test.png"/>'
            result = process_image_paths(html, Path(tmpdir))

            assert "data:image/png;base64," in result
            assert "test.png" not in result

    def test_embeds_relative_path_image(self):
        """Test embedding an image with relative path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create images subdirectory
            images_dir = Path(tmpdir) / "images"
            images_dir.mkdir()

            image_path = images_dir / "photo.png"
            image_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 50
            image_path.write_bytes(image_data)

            html = '<img src="images/photo.png"/>'
            result = process_image_paths(html, Path(tmpdir))

            assert "data:image/png;base64," in result

    def test_embeds_absolute_path_image(self):
        """Test embedding an image with absolute path."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            image_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 50
            f.write(image_data)
            f.flush()

            html = f'<img src="{f.name}"/>'
            result = process_image_paths(html, Path("/tmp"))

            assert "data:image/png;base64," in result

    def test_embeds_remote_image(self):
        """Test embedding a remote image."""
        mock_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 50

        mock_response = MagicMock()
        mock_response.read.return_value = mock_data
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_response):
            html = '<img src="https://example.com/image.png"/>'
            result = process_image_paths(html, Path("/tmp"))

            assert "data:image/png;base64," in result
            assert "https://example.com/image.png" not in result

    def test_preserves_img_attributes(self):
        """Test that other img attributes are preserved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image_path = Path(tmpdir) / "test.png"
            image_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 50
            image_path.write_bytes(image_data)

            html = '<img alt="Test Image" src="test.png" width="100"/>'
            result = process_image_paths(html, Path(tmpdir))

            assert 'alt="Test Image"' in result
            assert 'width="100"' in result
            assert "data:image/png;base64," in result

    def test_handles_missing_local_image(self, capsys):
        """Test warning for missing local images."""
        html = '<img src="missing.png"/>'
        result = process_image_paths(html, Path("/tmp"))

        # Should keep original src
        assert 'src="missing.png"' in result

        captured = capsys.readouterr()
        assert "Warning" in captured.err
        assert "Image not found" in captured.err

    def test_handles_failed_remote_fetch(self, capsys):
        """Test warning for failed remote image fetch."""
        import urllib.error

        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("test")):
            html = '<img src="https://example.com/image.png"/>'
            result = process_image_paths(html, Path("/tmp"))

            # Should keep original src
            assert 'src="https://example.com/image.png"' in result

            captured = capsys.readouterr()
            assert "Warning" in captured.err
            assert "Failed to fetch" in captured.err

    def test_processes_multiple_images(self):
        """Test processing multiple images in HTML."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test images
            for name in ["img1.png", "img2.png", "img3.png"]:
                image_path = Path(tmpdir) / name
                image_data = b"\x89PNG\r\n\x1a\n" + bytes(name, "ascii")
                image_path.write_bytes(image_data)

            html = '''
            <img src="img1.png"/>
            <p>Text</p>
            <img src="img2.png"/>
            <img src="img3.png"/>
            '''
            result = process_image_paths(html, Path(tmpdir))

            # Count data URIs
            assert result.count("data:image/png;base64,") == 3

    def test_verbose_output(self, capsys):
        """Test verbose output mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            image_path = Path(tmpdir) / "test.png"
            image_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 50
            image_path.write_bytes(image_data)

            html = '<img src="test.png"/>'
            process_image_paths(html, Path(tmpdir), verbose=True)

            captured = capsys.readouterr()
            assert "Embedded image:" in captured.out
            assert "Total images embedded:" in captured.out


class TestImageIntegration:
    """Integration tests for image embedding in PDF conversion."""

    def test_markdown_with_local_image_to_html(self):
        """Test that local images in Markdown are embedded in HTML."""
        from gospelo_md2pdf.converter import convert_md_to_html

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create images directory
            images_dir = Path(tmpdir) / "images"
            images_dir.mkdir()

            # Create a test image
            image_path = images_dir / "test.png"
            image_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
            image_path.write_bytes(image_data)

            # Create Markdown file
            md_content = """# Test Document

![Test Image](images/test.png)

Some text after image.
"""
            md_file = Path(tmpdir) / "test.md"
            md_file.write_text(md_content)

            output_dir = Path(tmpdir) / "output"
            html_content, _ = convert_md_to_html(md_file, output_dir)

            # Check that image was embedded
            assert "data:image/png;base64," in html_content
            assert "images/test.png" not in html_content

    def test_fixture_images(self):
        """Test using fixture images."""
        fixture_dir = Path(__file__).parent / "fixtures"
        images_dir = fixture_dir / "images"

        if not images_dir.exists():
            pytest.skip("Fixture images directory not found")

        # Check fixture images exist
        test_blue = images_dir / "test_blue.png"
        test_red = images_dir / "test_red.png"

        if not (test_blue.exists() and test_red.exists()):
            pytest.skip("Fixture images not found")

        html = f'''
        <img src="{test_blue}"/>
        <img src="{test_red}"/>
        '''
        result = process_image_paths(html, fixture_dir)

        assert result.count("data:image/png;base64,") == 2

    def test_sample_with_images_markdown(self):
        """Test the sample_with_images.md fixture."""
        from gospelo_md2pdf.converter import convert_md_to_html

        fixture_dir = Path(__file__).parent / "fixtures"
        md_file = fixture_dir / "sample_with_images.md"

        if not md_file.exists():
            pytest.skip("sample_with_images.md fixture not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            html_content, _ = convert_md_to_html(md_file, output_dir)

            # Check that images were embedded
            assert "data:image/png;base64," in html_content
            # Should have 2 images
            assert html_content.count("data:image/png;base64,") == 2
