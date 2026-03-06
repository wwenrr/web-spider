from datetime import datetime
from html import escape

from nicegui import ui

from infrastructure.models.category_crawl_job import CategoryCrawlJob


def render_category_jobs_panel(jobs: list[CategoryCrawlJob]) -> None:
    with ui.element("section").classes("spy-category-jobs-card"):
        with ui.element("div").classes("spy-category-jobs-head"):
            _render_text("h3", "Category Crawl Jobs", "spy-category-jobs-title")
            _render_text(
                "p",
                "Queue a category crawl to discover product detail URLs and fan them out into the detail spider queue.",
                "spy-category-jobs-note muted",
            )

        if not jobs:
            _render_text("span", "No category crawl jobs yet.", "todo-empty")
            return

        with ui.element("div").classes("spy-category-jobs-table-wrap"):
            with ui.element("table").classes("spy-category-jobs-table"):
                with ui.element("thead"):
                    with ui.element("tr"):
                        _render_text("th", "Category", "spy-category-jobs-th")
                        _render_text("th", "Status", "spy-category-jobs-th")
                        _render_text("th", "Products", "spy-category-jobs-th")
                        _render_text("th", "Per Page", "spy-category-jobs-th")
                        _render_text("th", "Pages", "spy-category-jobs-th")
                        _render_text("th", "Enqueued", "spy-category-jobs-th")
                        _render_text("th", "Crawl At", "spy-category-jobs-th")
                        _render_text("th", "Error", "spy-category-jobs-th")

                with ui.element("tbody"):
                    for job in jobs:
                        _render_job_row(job)


def _render_job_row(job: CategoryCrawlJob) -> None:
    with ui.element("tr"):
        with ui.element("td").classes("spy-category-jobs-td"):
            with ui.element("div").classes("spy-category-jobs-name-wrap"):
                _render_text("span", job.category_name, "spy-category-jobs-name")
                with ui.element("a").classes("spy-category-jobs-link").props(
                    f'href="{escape(job.category_url)}" target="_blank" rel="noreferrer noopener"'
                ):
                    _render_text("span", job.category_url, "spy-category-jobs-link-label")
        _render_text("td", job.crawl_status, f"spy-category-jobs-td spy-category-jobs-status spy-category-jobs-status--{job.crawl_status}")
        _render_text("td", _format_metric(job.total_products), "spy-category-jobs-td spy-category-jobs-td--mono")
        _render_text("td", _format_metric(job.products_per_page), "spy-category-jobs-td spy-category-jobs-td--mono")
        _render_text("td", _format_metric(job.total_pages), "spy-category-jobs-td spy-category-jobs-td--mono")
        _render_text("td", _format_metric(job.enqueued_products_count), "spy-category-jobs-td spy-category-jobs-td--mono")
        _render_text("td", _format_time(job.crawl_at), "spy-category-jobs-td spy-category-jobs-td--mono")
        _render_text("td", str(job.error_message or "-"), "spy-category-jobs-td spy-category-jobs-error")


def _render_text(tag: str, text: str, classes: str) -> None:
    with ui.element(tag).classes(classes):
        ui.html(escape(text))


def _format_metric(value: object) -> str:
    if value is None:
        return "-"
    return str(value)


def _format_time(raw_time: object) -> str:
    if isinstance(raw_time, datetime):
        return raw_time.strftime("%d/%m/%Y %H:%M:%S")

    normalized = str(raw_time or "").strip()
    if normalized == "":
        return "-"
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return normalized
    return parsed.strftime("%d/%m/%Y %H:%M:%S")
