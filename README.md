# mdformat-editorconfig

[![Build Status][ci-badge]][ci-link]
[![PyPI version][pypi-badge]][pypi-link]

An [mdformat](https://github.com/executablebooks/mdformat) plugin that applies [EditorConfig](https://editorconfig.org/) indentation settings to Markdown formatting.

> **Status: Work in Progress** - This plugin is under active development.

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

### Supported Properties

| Property | Values | Description |
|----------|--------|-------------|
| `indent_style` | `space`, `tab` | Type of indentation |
| `indent_size` | integer | Number of columns per indentation level |

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
