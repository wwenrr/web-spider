from collections.abc import Callable
from html import escape
from urllib.parse import urlsplit, urlunsplit

from nicegui import ui

SPY_1999_BASE_URL = "https://www.1999.co.jp"


def render_category_cards(
    categories: list[dict[str, object]],
    on_crawl: Callable[[str, str], None] | None = None,
    active_status_by_url: dict[str, str] | None = None,
) -> None:
    with ui.element("div").classes("spy-categories"):
        for category in categories:
            name = str(category.get("name", "Unnamed")).strip() or "Unnamed"
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
                        normalized_url = _normalize_category_url(full_url)
                        active_status = (active_status_by_url or {}).get(normalized_url)
                        with ui.element("li").classes("spy-sub-item"):
                            with ui.element("div").classes("spy-sub-main"):
                                with ui.element("a").classes("spy-sub-link").props(
                                    f'href="{escape(full_url)}" target="_blank" rel="noreferrer noopener"'
                                ):
                                    _render_text("span", label, "spy-sub-label")
                                _render_text("code", href, "spy-sub-href")
                            with ui.element("div").classes("spy-sub-actions"):
                                if active_status:
                                    _render_text("span", active_status, f"spy-sub-status spy-sub-status--{active_status}")
                                if on_crawl is not None:
                                    button_classes = "spy-sub-crawl spy-sub-crawl--disabled" if active_status else "spy-sub-crawl"
                                    button_props = "type=button disabled" if active_status else "type=button"
                                    button = ui.element("button").classes(button_classes).props(button_props)
                                    if not active_status:
                                        button.on(
                                            "click",
                                            lambda _event=None, crawl_name=f"{name} / {label}", crawl_url=full_url: on_crawl(
                                                crawl_name,
                                                crawl_url,
                                            ),
                                        )
                                    with button:
                                        _render_text("span", "Queued" if active_status else "Crawl", "spy-sub-crawl-label")


def _render_text(tag: str, text: str, classes: str) -> None:
    with ui.element(tag).classes(classes):
        ui.html(escape(text))


def _normalize_category_url(url: str) -> str:
    parts = urlsplit(url.strip())
    normalized_path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme, parts.netloc, normalized_path, parts.query, ""))
