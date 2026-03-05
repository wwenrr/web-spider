from html import escape

from nicegui import ui

SPY_1999_BASE_URL = "https://www.1999.co.jp"


def render_category_cards(categories: list[dict[str, object]]) -> None:
    with ui.element("div").classes("spy-categories"):
        for category in categories:
            name = str(category.get("name", "Unnamed"))
            raw_sub_items = category.get("sub", [])
            sub_items = raw_sub_items if isinstance(raw_sub_items, list) else []
            with ui.element("section").classes("spy-cat-card"):
                with ui.element("div").classes("spy-cat-head"):
                    _render_text("h3", name, "spy-cat-title")
                    _render_text("span", f"{len(sub_items)} links", "spy-cat-count")

                with ui.element("ul").classes("spy-sub-list"):
                    for item in sub_items:
                        if not isinstance(item, dict):
                            continue
                        href = str(item.get("href", "")).strip()
                        label = str(item.get("label", "Untitled")).strip()
                        full_url = f"{SPY_1999_BASE_URL}{href}" if href.startswith("/") else href
                        with ui.element("li").classes("spy-sub-item"):
                            with ui.element("a").classes("spy-sub-link").props(
                                f'href="{escape(full_url)}" target="_blank" rel="noreferrer noopener"'
                            ):
                                _render_text("span", label, "spy-sub-label")
                            _render_text("code", href, "spy-sub-href")


def _render_text(tag: str, text: str, classes: str) -> None:
    with ui.element(tag).classes(classes):
        ui.html(escape(text))
