from nicegui import ui

from ui.constants import PAGE_TITLE
from ui.layout import build_page
from ui.pages.cdp_connections.index import render_cdp_connection_crud_section
from ui.pages.dashboard.index import render_dashboard_section
from ui.pages.monitor.index import render_monitor_section
from ui.pages.spy_1999.products import render_products_crawl_section
from ui.pages.spy_1999.index import render_spy_1999_section


def render_standard_page(page_key: str, title: str, subtitle: str) -> None:
    ui.page_title(PAGE_TITLE)
    body = build_page(
        page=page_key,
        title=title,
        subtitle=subtitle,
    )
    with body:
        _render_view_content(page_key)


def render_spy_page(page_key: str, title: str, subtitle: str, active_tab: str) -> None:
    ui.page_title(PAGE_TITLE)
    body = build_page(
        page=page_key,
        title=title,
        subtitle=subtitle,
    )
    with body:
        render_spy_1999_section(initial_tab=active_tab)


def _render_view_content(page_key: str) -> None:
    if page_key == "dashboard":
        render_dashboard_section()
        return
    if page_key == "cdp_connections":
        render_cdp_connection_crud_section()
        return
    if page_key == "monitor":
        render_monitor_section()
        return
    if page_key == "products_crawl":
        render_products_crawl_section()
        return
    if page_key == "spy_1999":
        render_spy_1999_section()
        return
    render_dashboard_section()
