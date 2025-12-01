# mdformat-editorconfig

An mdformat plugin for applying `.editorconfig` indentation settings to Markdown formatting.

## Project Goal

Override mdformat's default 2-space indentation by reading settings from `.editorconfig` files. This allows users to configure their preferred indentation style (e.g., 4 spaces) via the standard EditorConfig mechanism.

## Target Properties

- `indent_style`: `space` or `tab`
- `indent_size`: Number of columns per indentation level

## Key Dependencies

- **mdformat**: The Markdown formatter this plugin extends
- **editorconfig** (editorconfig-core-py): Python library for parsing `.editorconfig` files

## Plugin Architecture

mdformat plugins use two main hooks:

1. **`update_mdit(mdit)`**: Modify the markdown-it parser (not needed for this plugin)
2. **`RENDERERS`**: Dict mapping token types to custom render functions

To customize indentation, override renderers for:
- `bullet_list`: Unordered list indentation
- `ordered_list`: Ordered list indentation
- `blockquote`: Blockquote continuation indentation

## Implementation Notes

- EditorConfig files are discovered by walking up from the file being formatted
- The `editorconfig.get_properties(filepath)` function handles discovery and parsing
- Challenge: mdformat renderers don't receive file path context by default; may need to use module-level state or context threading

## Reference Documentation

The `dev/` folder contains reference documentation:
- `dev/mdformat/`: mdformat plugin development docs
- `dev/editorconfig/`: EditorConfig specification

## Development Commands

```bash
# Install in development mode
uv pip install -e .

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=mdformat_editorconfig
```
