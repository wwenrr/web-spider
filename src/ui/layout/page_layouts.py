from nicegui import ui

from ui.layout.global_layout import build_shell


def build_page(page: str, title: str, subtitle: str) -> ui.column:
    return build_shell(page=page, title=title, subtitle=subtitle)
