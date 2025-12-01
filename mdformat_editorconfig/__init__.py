"""An mdformat plugin for applying .editorconfig indentation settings."""

__version__ = "0.1.0"

from mdformat_editorconfig.plugin import RENDERERS, update_mdit

__all__ = ["RENDERERS", "update_mdit"]
