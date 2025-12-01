"""mdformat-editorconfig plugin implementation.

Provides custom renderers that apply indentation settings from .editorconfig files.
"""

from typing import Mapping

from markdown_it import MarkdownIt
from mdformat.renderer import RenderContext, RenderTreeNode
from mdformat.renderer.typing import Render
from mdformat.renderer._context import get_list_marker_type, is_tight_list

from mdformat_editorconfig.config import get_indent_config


def update_mdit(mdit: MarkdownIt) -> None:
    """Update the markdown-it parser.

    This hook can be used to add markdown-it plugins or modify parser behavior.
    Currently a no-op for this plugin.
    """
    pass


def _get_indent(default_width: int) -> tuple[str, int]:
    """Get the indentation string and width based on editorconfig.

    Args:
        default_width: The default indent width (from marker length).

    Returns:
        Tuple of (indent_string, indent_width) where:
        - indent_string: The string to use for indentation
        - indent_width: The width in columns (for context.indented)
    """
    config = get_indent_config()
    if config is None:
        # No editorconfig - use default (passthrough behavior)
        return (" " * default_width, default_width)

    style, size = config
    if style == "tab":
        return ("\t", size)  # Tab char, but track column width
    else:
        return (" " * size, size)


def _bullet_list(node: RenderTreeNode, context: RenderContext) -> str:
    """Render a bullet list with configurable indentation."""
    marker_type = get_list_marker_type(node)
    first_line_indent = " "
    default_indent_width = len(marker_type + first_line_indent)

    indent_str, indent_width = _get_indent(default_indent_width)
    block_separator = "\n" if is_tight_list(node) else "\n\n"

    with context.indented(indent_width):
        text = ""
        for child_idx, child in enumerate(node.children):
            list_item = child.render(context)
            formatted_lines = []
            line_iterator = iter(list_item.split("\n"))
            first_line = next(line_iterator)
            formatted_lines.append(
                f"{marker_type}{first_line_indent}{first_line}"
                if first_line
                else marker_type
            )
            for line in line_iterator:
                formatted_lines.append(f"{indent_str}{line}" if line else "")

            text += "\n".join(formatted_lines)
            if child_idx != len(node.children) - 1:
                text += block_separator

        return text


def _ordered_list(node: RenderTreeNode, context: RenderContext) -> str:
    """Render an ordered list with configurable indentation."""
    consecutive_numbering = context.options.get("mdformat", {}).get("number", False)
    marker_type = get_list_marker_type(node)
    first_line_indent = " "
    block_separator = "\n" if is_tight_list(node) else "\n\n"
    list_len = len(node.children)

    starting_number = node.attrs.get("start")
    if starting_number is None:
        starting_number = 1
    assert isinstance(starting_number, int)

    # Calculate default indent width based on number width
    if consecutive_numbering:
        default_indent_width = len(
            f"{list_len + starting_number - 1}{marker_type}{first_line_indent}"
        )
    else:
        default_indent_width = len(f"{starting_number}{marker_type}{first_line_indent}")

    indent_str, indent_width = _get_indent(default_indent_width)

    text = ""
    with context.indented(indent_width):
        for list_item_index, list_item in enumerate(node.children):
            list_item_text = list_item.render(context)
            formatted_lines = []
            line_iterator = iter(list_item_text.split("\n"))
            first_line = next(line_iterator)
            if consecutive_numbering:
                number = starting_number + list_item_index
                pad = len(str(list_len + starting_number - 1))
                number_str = str(number).rjust(pad, "0")
                formatted_lines.append(
                    f"{number_str}{marker_type}{first_line_indent}{first_line}"
                    if first_line
                    else f"{number_str}{marker_type}"
                )
            else:
                first_item_marker = f"{starting_number}{marker_type}"
                other_item_marker = (
                    "0" * (len(str(starting_number)) - 1) + "1" + marker_type
                )
                if list_item_index == 0:
                    formatted_lines.append(
                        f"{first_item_marker}{first_line_indent}{first_line}"
                        if first_line
                        else first_item_marker
                    )
                else:
                    formatted_lines.append(
                        f"{other_item_marker}{first_line_indent}{first_line}"
                        if first_line
                        else other_item_marker
                    )
            for line in line_iterator:
                formatted_lines.append(indent_str + line if line else "")

            text += "\n".join(formatted_lines)
            if list_item_index != len(node.children) - 1:
                text += block_separator

        return text


# A mapping from syntax tree node type to a function that renders it.
# This can be used to overwrite renderer functions of existing syntax
# or add support for new syntax.
RENDERERS: Mapping[str, Render] = {
    "bullet_list": _bullet_list,
    "ordered_list": _ordered_list,
}
