"""An mdformat plugin for applying .editorconfig indentation settings."""

__version__ = "0.1.0"

from mdformat_editorconfig.config import (
    get_current_file,
    get_indent_config,
    set_current_file,
)
from mdformat_editorconfig.plugin import RENDERERS, update_mdit

__all__ = [
    "RENDERERS",
    "update_mdit",
    "set_current_file",
    "get_current_file",
    "get_indent_config",
]
