from nicegui import ui

from domain.jobs.services import list_jobs
from ui.constants import PAGE_TITLE, ROUTE_DASHBOARD
from ui.layout import build_page


def register_dashboard_page() -> None:
    @ui.page(ROUTE_DASHBOARD)
    def dashboard_page() -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(page="dashboard", title="Dashboard", subtitle="Overview of AI usage.")
        with body:
            jobs = list_jobs()
            ui.label(f"Total jobs: {len(jobs)}").classes("h2")
            ui.label("Data source: domain.jobs.services").classes("muted")
