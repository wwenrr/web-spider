from fastapi import Request
from nicegui import ui

from ui.components.forms import render_crawl_form
from ui.constants import PAGE_TITLE, ROUTE_CRAWL_PAGE
from ui.layout import build_page


def register_crawl_page() -> None:
    @ui.page(ROUTE_CRAWL_PAGE)
    def crawl_page(request: Request) -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(
            page="crawl",
            title="Crawl Settings",
            subtitle="Route-first URL with query support for source target.",
        )
        with body:
            render_crawl_form(_parse_site(request))


def _parse_site(request: Request) -> str:
    raw_query = request.url.query
    site = request.query_params.get("site")
    if site is None and raw_query and "=" not in raw_query:
        site = raw_query
    return site if site and site.strip() else "tiki"
