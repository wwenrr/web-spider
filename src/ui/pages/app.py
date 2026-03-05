from dataclasses import dataclass

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui

from ui.constants import (
    PAGE_TITLE,
    ROUTE_CDP_CONNECTIONS,
    ROUTE_DASHBOARD,
    ROUTE_MONITOR,
    ROUTE_ROOT,
    ROUTE_TODO,
)
from ui.layout import build_page
from ui.pages.cdp_connections import render_cdp_connection_crud_section
from ui.pages.dashboard import render_dashboard_section
from ui.pages.monitor import _refresh_monitor_page, render_monitor_section
from ui.pages.todos import render_todo_crud_section

LEGACY_CDP_ROUTE = "/cdp-connections"
DEFAULT_ROUTE = ROUTE_CDP_CONNECTIONS


@dataclass(frozen=True)
class PageConfig:
    key: str
    title: str
    subtitle: str


PAGE_CONFIGS: dict[str, PageConfig] = {
    "dashboard": PageConfig(
        key="dashboard",
        title="Dashboard",
        subtitle="Overview of AI usage.",
    ),
    "todo": PageConfig(
        key="todo",
        title="Todo CRUD",
        subtitle="Create, update, and manage todo items in one place.",
    ),
    "cdp_connections": PageConfig(
        key="cdp_connections",
        title="CDP Connections",
        subtitle="Manage remote Chrome DevTools Protocol endpoints in one place.",
    ),
    "monitor": PageConfig(
        key="monitor",
        title="Job Monitor",
        subtitle="Monitor queue jobs and worker operations in one place.",
    ),
}

VIEW_TO_ROUTE: dict[str, str] = {
    "dashboard": ROUTE_DASHBOARD,
    "todo": ROUTE_TODO,
    "cdp_connections": DEFAULT_ROUTE,
    "monitor": ROUTE_MONITOR,
}


def register_app_page() -> None:
    @ui.page(ROUTE_ROOT)
    def root_page(request: Request) -> RedirectResponse:
        view = request.query_params.get("view", "").strip().lower()
        if view in VIEW_TO_ROUTE:
            return RedirectResponse(VIEW_TO_ROUTE[view])
        return RedirectResponse(DEFAULT_ROUTE)

    @ui.page(ROUTE_DASHBOARD)
    def dashboard_page() -> None:
        _render_page(PAGE_CONFIGS["dashboard"])

    @ui.page(ROUTE_TODO)
    def todo_page() -> None:
        _render_page(PAGE_CONFIGS["todo"])

    @ui.page(DEFAULT_ROUTE)
    def cdp_connections_page() -> None:
        _render_page(PAGE_CONFIGS["cdp_connections"])

    @ui.page(LEGACY_CDP_ROUTE)
    def cdp_connections_kebab_alias() -> RedirectResponse:
        return RedirectResponse(DEFAULT_ROUTE)

    @ui.page(ROUTE_MONITOR)
    def monitor_page() -> None:
        _render_page(PAGE_CONFIGS["monitor"])
        ui.timer(5.0, _refresh_monitor_page)


def _render_page(page_config: PageConfig) -> None:
    ui.page_title(PAGE_TITLE)
    body = build_page(
        page=page_config.key,
        title=page_config.title,
        subtitle=page_config.subtitle,
    )
    with body:
        _render_view_content(page_config.key)


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
    render_todo_crud_section()
