from collections.abc import Callable

from nicegui import ui

from ui.constants import (
    ROUTE_CDP_CONNECTIONS,
    ROUTE_DASHBOARD,
    ROUTE_MANAGED_BROWSERS,
    ROUTE_MONITOR,
    ROUTE_PRODUCTS_CRAWL,
    ROUTE_SPY_1999,
    SIDEBAR_LOGO_HTML,
)


def build_shell(
    page: str,
    title: str,
    subtitle: str,
    on_navigate: Callable[[str], None] | None = None,
) -> ui.element:
    with ui.element("div").classes("shell"):
        _render_sidebar(page, on_navigate=on_navigate)
        with ui.element("div").classes("content"):
            with ui.element("div").classes("content-inner"):
                with ui.element("div").classes("page-hdr"):
                    with ui.element("div").classes("page-hdr-text"):
                        ui.label(title).classes("page-title")
                        ui.label(subtitle).classes("page-sub")
                body = ui.element("div").classes("page-body")
    return body


def _render_sidebar(page: str, on_navigate: Callable[[str], None] | None = None) -> None:
    with ui.element("nav").classes("nav"):
        with ui.element("div").classes("nav-head"):
            ui.html(
                f'<div class="nav-logo">{SIDEBAR_LOGO_HTML}</div>',
                sanitize=False,
            )
            with ui.element("div").classes("nav-brand"):
                ui.label("Web Spider").classes("nav-brand-title")
                ui.label("Automation Console").classes("nav-brand-sub")

        _render_link("Dashboard", "dashboard", ROUTE_DASHBOARD, "dashboard", page == "dashboard", on_navigate)

        ui.label("SPY").classes("nav-section")
        _render_link("1999.co.jp", "travel_explore", ROUTE_SPY_1999, "spy_1999", page == "spy_1999", on_navigate)
        _render_link(
            "Products Crawl",
            "inventory_2",
            ROUTE_PRODUCTS_CRAWL,
            "products_crawl",
            page == "products_crawl",
            on_navigate,
        )

        ui.label("OPERATIONS").classes("nav-section")
        _render_link(
            "CDP Connections",
            "lan",
            ROUTE_CDP_CONNECTIONS,
            "cdp_connections",
            page == "cdp_connections",
            on_navigate,
        )
        _render_link(
            "Managed Browsers",
            "web",
            ROUTE_MANAGED_BROWSERS,
            "managed_browsers",
            page == "managed_browsers",
            on_navigate,
        )

        ui.label("MONITOR").classes("nav-section")
        _render_link("Job Monitor", "monitor", ROUTE_MONITOR, "monitor", page == "monitor", on_navigate)

        ui.element("div").classes("nav-grow")


def _render_link(
    label: str,
    icon: str,
    href: str,
    page_key: str,
    active: bool,
    on_navigate: Callable[[str], None] | None = None,
    disabled: bool = False,
) -> None:
    cls = "nav-item nav-item--on" if active else "nav-item"
    if disabled:
        with ui.element("div").classes(f"{cls} nav-item--disabled"):
            with ui.element("span").classes("nav-item-ic-wrap"):
                ui.icon(icon).classes("nav-item-ic")
            ui.label(label).classes("nav-item-lbl")
            ui.label("Soon").classes("nav-item-tag")
        return

    if on_navigate is not None:
        with ui.element("button").classes(f"{cls} nav-btn-reset").on(
            "click", lambda _event=None, target=page_key: on_navigate(target)
        ):
            with ui.element("span").classes("nav-item-ic-wrap"):
                ui.icon(icon).classes("nav-item-ic")
            ui.label(label).classes("nav-item-lbl")
        return

    with ui.link(target=href).classes(cls):
        with ui.element("span").classes("nav-item-ic-wrap"):
            ui.icon(icon).classes("nav-item-ic")
        ui.label(label).classes("nav-item-lbl")
