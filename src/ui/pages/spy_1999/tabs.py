from html import escape

from nicegui import ui

from ui.constants import ROUTE_SPY_1999

SPY_TAB_CATEGORIES = "categories"
SPY_TAB_RANKINGS = "rankings"


def render_spy_tabs(active_tab: str) -> None:
    with ui.element("div").classes("spy-tabs"):
        _render_tab_link(
            label="1999 Categories",
            active=active_tab == SPY_TAB_CATEGORIES,
            href=_build_tab_href(SPY_TAB_CATEGORIES),
        )
        _render_tab_link(
            label="1999 Ranking",
            active=active_tab == SPY_TAB_RANKINGS,
            href=_build_tab_href(SPY_TAB_RANKINGS),
        )
        _render_tab_button(
            label="Crawler (Soon)",
            active=False,
            disabled=True,
        )


def _build_tab_href(tab: str) -> str:
    return f"{ROUTE_SPY_1999}?tab={tab}"


def _render_tab_link(
    label: str,
    active: bool,
    href: str,
) -> None:
    classes = "spy-tab-btn spy-tab-btn--active" if active else "spy-tab-btn"

    with ui.link(target=href).classes(classes).props('style="text-decoration:none"'):
        _render_text("span", label, "spy-tab-label")


def _render_tab_button(
    label: str,
    active: bool,
    disabled: bool = False,
) -> None:
    classes = "spy-tab-btn spy-tab-btn--active" if active else "spy-tab-btn"
    if disabled:
        classes = f"{classes} spy-tab-btn--disabled"

    disabled_prop = "type=button disabled" if disabled else "type=button"
    with ui.element("button").classes(classes).props(disabled_prop):
        _render_text("span", label, "spy-tab-label")


def _render_text(tag: str, text: str, classes: str) -> None:
    with ui.element(tag).classes(classes):
        ui.html(escape(text))
