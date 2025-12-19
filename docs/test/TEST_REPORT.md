# Test Report - gospelo-md2pdf

Generated: 2025-12-19

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | 46 |
| Passed | 46 |
| Failed | 0 |
| Skipped | 0 |
| Coverage | 83% |
| Test Duration | 13.74s |

## Test Environment

| Item | Value |
|------|-------|
| Platform | darwin (macOS) |
| Python | 3.12.8 |
| pytest | 7.4.4 |
| pytest-cov | 4.1.0 |

## Coverage by Module

| Module | Statements | Missing | Coverage |
|--------|------------|---------|----------|
| `__init__.py` | 3 | 0 | 100% |
| `__main__.py` | 3 | 3 | 0% |
| `cli.py` | 36 | 8 | 78% |
| `converter.py` | 73 | 12 | 84% |
| `mermaid.py` | 49 | 6 | 88% |
| `styles.py` | 13 | 1 | 92% |
| **TOTAL** | **177** | **30** | **83%** |

## Test Details

### test_cli.py (6 tests)

| Test | Status |
|------|--------|
| `TestCLI::test_help_option` | PASSED |
| `TestCLI::test_version_option` | PASSED |
| `TestCLI::test_missing_input_file` | PASSED |
| `TestCLI::test_basic_conversion` | PASSED |
| `TestCLI::test_quiet_mode` | PASSED |
| `TestCLI::test_no_html_option` | PASSED |

### test_converter.py (12 tests)

| Test | Status |
|------|--------|
| `TestGetOutputDir::test_explicit_output_dir` | PASSED |
| `TestGetOutputDir::test_env_variable` | PASSED |
| `TestGetOutputDir::test_default_to_cwd` | PASSED |
| `TestConvertMdToHtml::test_basic_conversion` | PASSED |
| `TestConvertMdToHtml::test_file_not_found` | PASSED |
| `TestConvertMdToHtml::test_table_conversion` | PASSED |
| `TestConvertMdToHtml::test_code_block_conversion` | PASSED |
| `TestConvertMdToHtml::test_custom_lang_attribute` | PASSED |
| `TestConvertMdToPdf::test_basic_pdf_generation` | PASSED |
| `TestConvertMdToPdf::test_html_file_kept_by_default` | PASSED |
| `TestConvertMdToPdf::test_html_file_removed_when_requested` | PASSED |
| `TestConvertMdToPdf::test_custom_output_file` | PASSED |

### test_mermaid.py (17 tests)

| Test | Status |
|------|--------|
| `TestCheckMermaidCli::test_returns_bool` | PASSED |
| `TestCheckMermaidCli::test_returns_false_when_not_installed` | PASSED |
| `TestCheckMermaidCli::test_returns_true_when_installed` | PASSED |
| `TestProcessMermaidBlocks::test_returns_unchanged_when_no_mermaid` | PASSED |
| `TestProcessMermaidBlocks::test_returns_unchanged_when_mermaid_cli_not_found` | PASSED |
| `TestProcessMermaidBlocks::test_processes_mermaid_blocks` | PASSED |
| `TestRenderMermaidToPng::test_renders_simple_diagram` | PASSED |
| `TestRenderMermaidToPng::test_renders_flowchart_with_japanese` | PASSED |
| `TestRenderMermaidToPng::test_returns_false_on_invalid_syntax` | PASSED |
| `TestMermaidIntegration::test_markdown_with_mermaid_to_html` | PASSED |
| `TestMermaidIntegration::test_markdown_with_mermaid_to_pdf` | PASSED |
| `TestMermaidIntegration::test_multiple_mermaid_diagrams` | PASSED |
| `TestMermaidIntegration::test_mermaid_with_japanese_text` | PASSED |
| `TestMermaidIntegration::test_mermaid_with_subgraph_quotes` | PASSED |
| `TestHtmlEntityUnescaping::test_unescape_html_entities` | PASSED |
| `TestHtmlEntityUnescaping::test_unescape_single_quotes` | PASSED |
| `TestHtmlEntityUnescaping::test_unescape_ampersand` | PASSED |

### test_styles.py (11 tests)

| Test | Status |
|------|--------|
| `TestDefaultCss::test_default_css_not_empty` | PASSED |
| `TestDefaultCss::test_default_css_contains_page_rule` | PASSED |
| `TestDefaultCss::test_default_css_contains_body_style` | PASSED |
| `TestDefaultCss::test_default_css_contains_special_classes` | PASSED |
| `TestDefaultCss::test_default_css_contains_mermaid_style` | PASSED |
| `TestGetDefaultCss::test_returns_css_from_file` | PASSED |
| `TestGetDefaultCss::test_fallback_to_constant_when_file_missing` | PASSED |
| `TestLoadCssFile::test_load_existing_css_file` | PASSED |
| `TestLoadCssFile::test_load_css_file_with_string_path` | PASSED |
| `TestLoadCssFile::test_load_nonexistent_css_file` | PASSED |
| `TestLoadCssFile::test_load_css_file_with_utf8_content` | PASSED |

## Uncovered Code

### `__main__.py` (0% coverage)

Entry point module - not directly tested as it delegates to `cli.main()`.

```python
# Lines 3-6
from .cli import main

if __name__ == "__main__":
    main()
```

### `cli.py` (78% coverage)

Missing lines: 106-113, 117 (main function execution block)

### `converter.py` (84% coverage)

Missing lines: Error handling paths and edge cases
- Line 67: Custom CSS file loading error
- Lines 88, 92, 97-99, 103: Various error handling paths
- Lines 129, 156, 163: Edge cases in conversion
- Lines 216, 230: PDF generation error handling

### `mermaid.py` (88% coverage)

Missing lines: 59-61, 122, 127, 132 (error handling for Mermaid CLI failures)

### `styles.py` (92% coverage)

Missing line: 352 (fallback to DEFAULT_CSS constant when bundled file missing)

## Running Tests

```bash
# Run all tests
DYLD_LIBRARY_PATH=/opt/homebrew/lib python -m pytest

# Run with coverage
DYLD_LIBRARY_PATH=/opt/homebrew/lib python -m pytest --cov=src/gospelo_md2pdf --cov-report=term-missing

# Run specific test file
DYLD_LIBRARY_PATH=/opt/homebrew/lib python -m pytest tests/test_mermaid.py -v

# Run tests matching a pattern
DYLD_LIBRARY_PATH=/opt/homebrew/lib python -m pytest -k "mermaid" -v
```

## Notes

1. **Mermaid tests require mermaid-cli**: Tests marked with `@pytest.mark.skipif(not check_mermaid_cli(), ...)` will be skipped if mermaid-cli is not installed.

2. **macOS library path**: On macOS, `DYLD_LIBRARY_PATH=/opt/homebrew/lib` is required for WeasyPrint to find system libraries.

3. **Coverage target**: The current coverage of 83% is considered sufficient for a v1.0 release. Uncovered code is primarily error handling and entry point code.

## Change History

| Date | Version | Tests | Coverage | Notes |
|------|---------|-------|----------|-------|
| 2025-01-19 | 1.0.0 | 42 | 83% | Initial release |
| 2025-12-19 | 1.0.1 | 46 | 83% | Added HTML entity unescaping tests |
