"""Tests for editorconfig integration."""

import tempfile
from pathlib import Path

import mdformat
import pytest

from mdformat_editorconfig import set_current_file


@pytest.fixture
def temp_project():
    """Create a temporary project directory with .editorconfig."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def create_editorconfig(project_dir: Path, content: str) -> None:
    """Create an .editorconfig file in the project directory."""
    editorconfig_path = project_dir / ".editorconfig"
    editorconfig_path.write_text(content)


def format_with_context(text: str, filepath: Path) -> str:
    """Format markdown text with file context set."""
    set_current_file(filepath)
    try:
        return mdformat.text(text, extensions={"editorconfig"})
    finally:
        set_current_file(None)


class TestFourSpaceIndent:
    """Tests for 4-space indentation."""

    def test_bullet_list_nested(self, temp_project):
        """Nested bullet lists should use 4-space indentation."""
        create_editorconfig(
            temp_project,
            """
root = true

[*.md]
indent_style = space
indent_size = 4
""",
        )
        md_file = temp_project / "test.md"

        input_text = """\
- Item 1
  - Nested item
- Item 2
"""
        expected = """\
- Item 1
    - Nested item
- Item 2
"""
        result = format_with_context(input_text, md_file)
        assert result == expected

    def test_bullet_list_continuation(self, temp_project):
        """Continuation lines should use 4-space indentation."""
        create_editorconfig(
            temp_project,
            """
root = true

[*.md]
indent_style = space
indent_size = 4
""",
        )
        md_file = temp_project / "test.md"

        input_text = """\
- Item 1
  with continuation
- Item 2
"""
        expected = """\
- Item 1
    with continuation
- Item 2
"""
        result = format_with_context(input_text, md_file)
        assert result == expected

    def test_ordered_list_nested(self, temp_project):
        """Nested ordered lists should use 4-space indentation."""
        create_editorconfig(
            temp_project,
            """
root = true

[*.md]
indent_style = space
indent_size = 4
""",
        )
        md_file = temp_project / "test.md"

        input_text = """\
1. Item 1
   1. Nested item
2. Item 2
"""
        # Note: mdformat uses "1." for all items by default (non-consecutive numbering)
        expected = """\
1. Item 1
    1. Nested item
1. Item 2
"""
        result = format_with_context(input_text, md_file)
        assert result == expected


class TestTabIndent:
    """Tests for tab indentation."""

    def test_bullet_list_with_tabs(self, temp_project):
        """Bullet lists should use tab indentation when configured."""
        create_editorconfig(
            temp_project,
            """
root = true

[*.md]
indent_style = tab
indent_size = 4
""",
        )
        md_file = temp_project / "test.md"

        input_text = """\
- Item 1
  - Nested item
- Item 2
"""
        expected = """\
- Item 1
\t- Nested item
- Item 2
"""
        result = format_with_context(input_text, md_file)
        assert result == expected


class TestNoEditorConfig:
    """Tests for behavior when no .editorconfig is present."""

    def test_passthrough_without_editorconfig(self, temp_project):
        """Without .editorconfig, use mdformat defaults (2 spaces)."""
        # No .editorconfig file created
        md_file = temp_project / "test.md"

        input_text = """\
- Item 1
    - Nested item
- Item 2
"""
        # mdformat default is 2-space indentation
        expected = """\
- Item 1
  - Nested item
- Item 2
"""
        result = format_with_context(input_text, md_file)
        assert result == expected


class TestCwdFallback:
    """Tests for cwd-based fallback when no file context is set."""

    def test_uses_cwd_editorconfig(self, temp_project, monkeypatch):
        """Without file context, should use .editorconfig from cwd."""
        create_editorconfig(
            temp_project,
            """
root = true

[*.md]
indent_style = space
indent_size = 4
""",
        )

        # Change to temp_project directory
        monkeypatch.chdir(temp_project)

        # Clear any existing file context
        set_current_file(None)

        input_text = """\
- Item 1
  - Nested item
- Item 2
"""
        expected = """\
- Item 1
    - Nested item
- Item 2
"""
        result = mdformat.text(input_text, extensions={"editorconfig"})
        assert result == expected

    def test_fallback_without_editorconfig(self, temp_project, monkeypatch):
        """Without .editorconfig in cwd, use mdformat defaults."""
        # No .editorconfig file created
        monkeypatch.chdir(temp_project)
        set_current_file(None)

        input_text = """\
- Item 1
    - Nested item
- Item 2
"""
        # mdformat default is 2-space indentation
        expected = """\
- Item 1
  - Nested item
- Item 2
"""
        result = mdformat.text(input_text, extensions={"editorconfig"})
        assert result == expected


class TestEditorConfigInheritance:
    """Tests for .editorconfig inheritance behavior."""

    def test_reads_parent_editorconfig(self, temp_project):
        """Should read .editorconfig from parent directories."""
        # Create .editorconfig in parent
        create_editorconfig(
            temp_project,
            """
root = true

[*.md]
indent_style = space
indent_size = 4
""",
        )

        # Create subdirectory
        subdir = temp_project / "docs"
        subdir.mkdir()
        md_file = subdir / "test.md"

        input_text = """\
- Item 1
  - Nested item
"""
        expected = """\
- Item 1
    - Nested item
"""
        result = format_with_context(input_text, md_file)
        assert result == expected
