# mdformat-editorconfig

[![Build Status][ci-badge]][ci-link]
[![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin that applies [EditorConfig](https://editorconfig.org/) indentation settings to Markdown formatting.

## Motivation

mdformat uses opinionated defaults for indentation (2 spaces). This plugin allows you to configure indentation via `.editorconfig` files, making mdformat respect your project's or personal indentation preferences.

## Installation

```bash
pip install mdformat-editorconfig
```

Or with [pipx](https://pipx.pypa.io/) for command-line usage:

```bash
pipx install mdformat
pipx inject mdformat mdformat-editorconfig
```

## Usage

Create an `.editorconfig` file in your project (or home directory):

```ini
# .editorconfig
root = true

[*.md]
indent_style = space
indent_size = 4
```

Then format your Markdown files as usual:

```bash
mdformat your-file.md
```

### Example

With the above `.editorconfig`, nested lists will use 4-space indentation:

**Before:**
```markdown
- Item 1
  - Nested item
- Item 2
```

**After:**
```markdown
- Item 1
    - Nested item
- Item 2
```

### Supported Properties

| Property | Values | Description |
|----------|--------|-------------|
| `indent_style` | `space`, `tab` | Type of indentation |
| `indent_size` | integer | Number of columns per indentation level |

## How It Works

The plugin overrides mdformat's list renderers to apply indentation settings from `.editorconfig` files. It:

1. Looks up `.editorconfig` settings based on the current working directory
2. Reads `indent_style` and `indent_size` properties
3. Applies the configured indentation to list continuation lines and nested content

### CLI Usage

When using mdformat from the command line, the plugin looks up `.editorconfig` settings based on your **current working directory**. This means:

- Run mdformat from your project root to pick up project-level `.editorconfig`
- A global `~/.editorconfig` (with `root = true`) will apply to all mdformat calls within your home directory

```bash
# Run from project root to use project's .editorconfig
cd /path/to/project
mdformat docs/*.md
```

### Limitation

Due to mdformat's plugin architecture, the plugin cannot determine the actual file path being formatted. Instead, it uses the current working directory for `.editorconfig` lookup. This works well for the common case of running mdformat from a project root, but may not pick up the correct settings if you format files from a different directory.

### Python API

When using the Python API directly, you can explicitly set the file context for more precise `.editorconfig` lookup:

```python
import mdformat
from mdformat_editorconfig import set_current_file

# Set the file context for editorconfig lookup
set_current_file("/path/to/your/file.md")
try:
    result = mdformat.text(markdown_text, extensions={"editorconfig"})
finally:
    set_current_file(None)
```

## Scope

This plugin currently handles indentation for:

- Bullet lists (unordered lists)
- Ordered lists

Code blocks and blockquotes follow CommonMark standard formatting (4-space indentation for indented code blocks).

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/jdmonaco/mdformat-editorconfig.git
cd mdformat-editorconfig

# Install development environment with uv
uv sync
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=mdformat_editorconfig

# Run tests verbosely
uv run pytest -v
```

## License

MIT - see LICENSE file for details.

[ci-badge]: https://github.com/jdmonaco/mdformat-editorconfig/workflows/CI/badge.svg
[ci-link]: https://github.com/jdmonaco/mdformat-editorconfig/actions?query=workflow%3ACI+branch%3Amain+event%3Apush
[pypi-badge]: https://img.shields.io/pypi/v/mdformat-editorconfig.svg
[pypi-link]: https://pypi.org/project/mdformat-editorconfig
