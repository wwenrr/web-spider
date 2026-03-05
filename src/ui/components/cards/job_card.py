from nicegui import ui

from domain.jobs.services import delete_job, toggle_job
from ui.components.badges import render_status_badge
from ui.constants import ROUTE_DASHBOARD, route_job_edit
from ui.helpers import format_datetime


def render_job_detail_card(todo: object) -> None:
    with ui.card().classes("card"):
        with ui.row().classes("w-full items-center justify-between"):
            title = getattr(todo, "title", "")
            is_done = bool(getattr(todo, "is_done", False))
            todo_id = int(getattr(todo, "id", 0))

            ui.label(str(title)).classes("h2")
            render_status_badge(is_done)

        with ui.column().classes("det-list"):
            _render_detail_row("Job ID", str(todo_id))
            _render_detail_row("Created", format_datetime(getattr(todo, "created_at", "")))
            _render_detail_row("Updated", format_datetime(getattr(todo, "updated_at", "")))

        with ui.row().classes("gap-3 mt-4"):
            ui.button("Edit", on_click=lambda: ui.navigate.to(route_job_edit(todo_id))).props(
                "unelevated no-caps size=sm"
            ).classes("btn-primary")
            ui.button("Toggle", on_click=lambda: _toggle_job(todo_id)).props(
                "outline no-caps size=sm"
            )
            ui.button("Delete", on_click=lambda: _delete_job(todo_id)).props(
                "flat no-caps color=red-7 size=sm"
            )
            ui.button("Back", on_click=lambda: ui.navigate.to(ROUTE_DASHBOARD)).props(
                "flat no-caps color=grey-7 size=sm"
            )


def render_job_not_found_card(todo_id: int) -> None:
    with ui.card().classes("card").style("border-color:#F5C6CB;background:#FFF5F5"):
        ui.label(f"Job #{todo_id} not found.").style("color:#C0392B")
        ui.button("Back to Dashboard", on_click=lambda: ui.navigate.to(ROUTE_DASHBOARD)).props(
            "flat no-caps color=grey-7 size=sm"
        )


def _render_detail_row(label: str, value: str) -> None:
    with ui.element("div").classes("det-row"):
        ui.label(label).classes("det-key")
        ui.label(value).classes("det-val")


def _toggle_job(todo_id: int) -> None:
    toggle_job(todo_id)
    ui.navigate.reload()


def _delete_job(todo_id: int) -> None:
    delete_job(todo_id)
    ui.navigate.to(ROUTE_DASHBOARD)
