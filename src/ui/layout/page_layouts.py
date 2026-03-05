from collections.abc import Callable

from nicegui import ui

from ui.layout.global_layout import build_shell


def build_page(
    page: str,
    title: str,
    subtitle: str,
    on_navigate: Callable[[str], None] | None = None,
) -> ui.column:
    return build_shell(page=page, title=title, subtitle=subtitle, on_navigate=on_navigate)
