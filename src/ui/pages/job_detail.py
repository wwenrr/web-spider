from nicegui import ui

from domain.jobs.services import get_job
from ui.components.cards import render_job_detail_card, render_job_not_found_card
from ui.components.forms import render_job_form
from ui.constants import PAGE_TITLE, ROUTE_JOB_DETAIL, ROUTE_JOB_EDIT
from ui.layout import build_page


def register_job_detail_pages() -> None:
    @ui.page(ROUTE_JOB_DETAIL)
    def show_job_page(todo_id: int) -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(
            page="jobs",
            title=f"Job #{todo_id}",
            subtitle="Review status, metadata, and run actions.",
        )
        with body:
            todo = get_job(todo_id)
            if todo is None:
                render_job_not_found_card(todo_id)
                return
            render_job_detail_card(todo)

    @ui.page(ROUTE_JOB_EDIT)
    def edit_job_page(todo_id: int) -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(
            page="jobs",
            title=f"Edit Job #{todo_id}",
            subtitle="Update title and keep campaign naming consistent.",
        )
        with body:
            todo = get_job(todo_id)
            if todo is None:
                render_job_not_found_card(todo_id)
                return
            render_job_form(mode="edit", todo_id=todo.id, current_title=todo.title)
