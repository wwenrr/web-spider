from ui.constants import PAGE_TITLE, ROUTE_MONITOR
from ui.layout import build_page
from ui.pages.monitor.sections import (
    refresh_monitor_live_sections,
    render_monitor_live_sections,
    render_observability_notes,
    render_pybgworker_cli,
)

from nicegui import ui


def register_monitor_page() -> None:
    @ui.page(ROUTE_MONITOR)
    def monitor_jobs_page() -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(
            page="monitor",
            title="Job Monitor",
            subtitle="Monitor queue jobs and worker operations in one place.",
        )
        with body:
            render_monitor_section()
            ui.timer(5.0, _refresh_monitor_page)


def render_monitor_section() -> None:
    render_monitor_live_sections()
    render_pybgworker_cli()
    render_observability_notes()


def _refresh_monitor_page() -> None:
    refresh_monitor_live_sections()
