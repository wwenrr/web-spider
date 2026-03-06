from collections.abc import Callable

from nicegui import ui

from core.category_crawls.facade import enqueue_category_crawl, list_category_crawl_jobs
from infrastructure.models.category_crawl_job import CategoryCrawlJob, CategoryCrawlStatus
from ui.data.spy_1999_categories import SPY_1999_CATEGORIES
from ui.data.spy_1999_rankings import SPY_1999_RANKING_CATEGORIES
from ui.helpers import show_error, show_success
from ui.pages.spy_1999.cards import render_category_cards
from ui.pages.spy_1999.category_jobs import render_category_jobs_panel
from ui.pages.spy_1999.tabs import SPY_TAB_CATEGORIES, SPY_TAB_RANKINGS, render_spy_tabs

_refresh_callback: Callable[[], None] | None = None


def render_spy_1999_section(initial_tab: str = SPY_TAB_CATEGORIES) -> None:
    active_tab = initial_tab if initial_tab in {SPY_TAB_CATEGORIES, SPY_TAB_RANKINGS} else SPY_TAB_CATEGORIES

    with ui.element("div").classes("spy-root"):
        render_spy_tabs(active_tab)
        if active_tab == SPY_TAB_RANKINGS:
            render_category_cards(SPY_1999_RANKING_CATEGORIES)
            return

        @ui.refreshable
        def render_categories_view() -> None:
            jobs = list_category_crawl_jobs(limit=20)
            render_category_jobs_panel(jobs)
            render_category_cards(
                SPY_1999_CATEGORIES,
                on_crawl=lambda category_name, category_url: _enqueue_category_job(
                    category_name=category_name,
                    category_url=category_url,
                    refresh_view=render_categories_view.refresh,
                ),
                active_status_by_url=_build_active_status_by_url(jobs),
            )

        render_categories_view()
        global _refresh_callback
        _refresh_callback = render_categories_view.refresh


def refresh_spy_1999_section() -> None:
    if _refresh_callback is not None:
        _refresh_callback()


def _enqueue_category_job(category_name: str, category_url: str, refresh_view: Callable[[], None]) -> None:
    try:
        enqueue_category_crawl(category_name=category_name, category_url=category_url)
    except ValueError as err:
        show_error(str(err))
        return

    refresh_view()
    show_success("Category crawl queued as pending.")


def _build_active_status_by_url(jobs: list[CategoryCrawlJob]) -> dict[str, str]:
    active_status_by_url: dict[str, str] = {}
    for job in jobs:
        if job.crawl_status not in {CategoryCrawlStatus.PENDING.value, CategoryCrawlStatus.PROCESSING.value}:
            continue
        active_status_by_url[job.normalized_category_url] = job.crawl_status
    return active_status_by_url
