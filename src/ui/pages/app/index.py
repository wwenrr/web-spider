from dataclasses import dataclass

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui

from ui.constants import (
    ROUTE_CDP_CONNECTIONS,
    ROUTE_DASHBOARD,
    ROUTE_MONITOR,
    ROUTE_PRODUCTS_CRAWL,
    ROUTE_ROOT,
    ROUTE_SPY_1999,
)
from ui.pages.app.renderers import render_spy_page, render_standard_page
from ui.pages.monitor.index import _refresh_monitor_page
from ui.pages.spy_1999.index import refresh_spy_1999_section
from ui.pages.spy_1999.products import refresh_products_crawl_section

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
    "products_crawl": PageConfig(
        key="products_crawl",
        title="Products Crawl",
        subtitle="Queue product page URLs and track crawl statuses.",
    ),
    "spy_1999": PageConfig(
        key="spy_1999",
        title="Spy 1999.co.jp",
        subtitle="Render discovered category and ranking links for crawl preparation.",
    ),
}

VIEW_TO_ROUTE: dict[str, str] = {
    "dashboard": ROUTE_DASHBOARD,
    "cdp_connections": DEFAULT_ROUTE,
    "monitor": ROUTE_MONITOR,
    "products_crawl": ROUTE_PRODUCTS_CRAWL,
    "spy_1999": ROUTE_SPY_1999,
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
        config = PAGE_CONFIGS["dashboard"]
        render_standard_page(config.key, config.title, config.subtitle)

    @ui.page(DEFAULT_ROUTE)
    def cdp_connections_page() -> None:
        config = PAGE_CONFIGS["cdp_connections"]
        render_standard_page(config.key, config.title, config.subtitle)

    @ui.page(LEGACY_CDP_ROUTE)
    def cdp_connections_kebab_alias() -> RedirectResponse:
        return RedirectResponse(DEFAULT_ROUTE)

    @ui.page(ROUTE_MONITOR)
    def monitor_page() -> None:
        config = PAGE_CONFIGS["monitor"]
        render_standard_page(config.key, config.title, config.subtitle)
        ui.timer(5.0, _refresh_monitor_page)

    @ui.page(ROUTE_PRODUCTS_CRAWL)
    def products_crawl_page() -> None:
        config = PAGE_CONFIGS["products_crawl"]
        render_standard_page(config.key, config.title, config.subtitle)
        ui.timer(5.0, refresh_products_crawl_section)

    @ui.page(ROUTE_SPY_1999)
    def spy_1999_page(request: Request) -> None:
        tab = request.query_params.get("tab", "").strip().lower()
        active_tab = tab if tab in {"categories", "rankings"} else "categories"
        config = PAGE_CONFIGS["spy_1999"]
        render_spy_page(config.key, config.title, config.subtitle, active_tab)
        if active_tab == "categories":
            ui.timer(5.0, refresh_spy_1999_section)
