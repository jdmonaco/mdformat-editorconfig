# mdformat-editorconfig

An mdformat plugin for applying `.editorconfig` indentation settings to Markdown formatting.

## Project Overview

This plugin overrides mdformat's default 2-space list indentation by reading `indent_style` and `indent_size` from `.editorconfig` files.

## Current Implementation

### Supported EditorConfig Properties

| Property | Status | Implementation |
|----------|--------|----------------|
| `indent_style` | ✅ Implemented | Space or tab indentation for lists |
| `indent_size` | ✅ Implemented | Configurable indent width |
| `tab_width` | ✅ Implemented | Used when `indent_size = tab` |
| `trim_trailing_whitespace` | N/A | Always enabled by mdformat core |
| `insert_final_newline` | N/A | Always enabled by mdformat core |
| `charset` | N/A | Outside formatter scope |
| `end_of_line` | N/A | Use mdformat's `--end-of-line` option |

### Architecture

```
mdformat_editorconfig/
├── __init__.py    # Public API exports, version
├── config.py      # EditorConfig lookup, file context tracking
└── plugin.py      # Custom list renderers (RENDERERS dict)
```

**Key components:**

- **`config.py`**: Uses `contextvars` for thread-safe file path tracking. Falls back to `Path.cwd() / "_.md"` for CLI usage when no explicit file context is set.
- **`plugin.py`**: Overrides `bullet_list` and `ordered_list` renderers to apply configured indentation.

### Known Limitations

1. **CLI file path**: mdformat doesn't pass file paths to renderers. Plugin uses cwd-based lookup as fallback.
2. **Scope**: Only list indentation is configurable. Code blocks and blockquotes use standard formatting.
3. **Core behaviors**: `trim_trailing_whitespace` and `insert_final_newline` cannot be disabled (mdformat design).

## Key Dependencies

- **mdformat** (>=0.7.0): The Markdown formatter
- **editorconfig** (>=0.12.0): EditorConfig file parsing

## Plugin Extension Points

mdformat plugins can use:

1. **`RENDERERS`**: Dict mapping node types to render functions (what we use)
2. **`update_mdit(mdit)`**: Modify the markdown-it parser (not needed here)

**Cannot override:** Post-processing, final newline handling, trailing whitespace trimming.

## Future Enhancement Ideas

- Support additional node types if mdformat exposes them
- Investigate mdformat hook proposals for file path access
- Consider wrapper tool for properties outside plugin scope

## Development

```bash
uv sync                                    # Install dependencies
uv run pytest                              # Run tests
uv run pytest --cov=mdformat_editorconfig  # Run with coverage
```

## Release Process

1. Update version in `__init__.py`
2. Commit changes
3. Tag with `git tag vX.Y.Z`
4. Push tag to trigger PyPI publish: `git push origin vX.Y.Z`

## Reference Documentation

The `dev/` folder contains reference documentation:
- `dev/mdformat/`: mdformat plugin development docs
- `dev/editorconfig/`: EditorConfig specification
