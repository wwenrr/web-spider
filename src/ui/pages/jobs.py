from fastapi.responses import RedirectResponse
from nicegui import ui

from ui.components.forms import render_job_form
from ui.constants import PAGE_TITLE, ROUTE_DASHBOARD, ROUTE_JOB_CREATE, ROUTE_ROOT
from ui.layout import build_page


def register_jobs_pages() -> None:
    @ui.page(ROUTE_ROOT)
    def root_page() -> RedirectResponse:
        return RedirectResponse(ROUTE_DASHBOARD)

    @ui.page(ROUTE_JOB_CREATE)
    def create_job_page() -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(
            page="create",
            title="Create Job",
            subtitle="Create a new campaign item and start processing.",
        )
        with body:
            ui.separator().classes("page-top-sep")
            render_job_form(mode="create")
