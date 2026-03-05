from nicegui import ui

from domain.jobs.services import create_job_with_audit, update_job
from ui.constants import ROUTE_DASHBOARD, route_job_detail
from ui.helpers import show_error


def render_job_form(mode: str, todo_id: int | None = None, current_title: str = "") -> None:
    with ui.card().classes("card"):
        ui.label("Job Title").classes("field-label")
        field = ui.input(
            placeholder="e.g. software development competition for students",
            value=current_title,
        ).classes("w-full")
        field.props("outlined dense")

        with ui.row().classes("gap-3 mt-4"):
            if mode == "create":
                ui.button("Save Job", on_click=lambda: _save_job(field.value)).props(
                    "unelevated no-caps size=sm"
                ).classes("btn-primary")
                ui.button("Cancel", on_click=lambda: ui.navigate.to(ROUTE_DASHBOARD)).props(
                    "flat no-caps color=grey-7 size=sm"
                )
                return

            if todo_id is None:
                show_error("Missing todo_id for edit mode")
                return

            ui.button("Update Job", on_click=lambda job_id=todo_id: _update_job(job_id, field.value)).props(
                "unelevated no-caps size=sm"
            ).classes("btn-primary")
            ui.button("Cancel", on_click=lambda job_id=todo_id: ui.navigate.to(route_job_detail(job_id))).props(
                "flat no-caps color=grey-7 size=sm"
            )


def _save_job(raw: str | None) -> None:
    title = (raw or "").strip()
    try:
        create_job_with_audit(title)
    except ValueError as err:
        show_error(str(err))
        return

    ui.navigate.to(ROUTE_DASHBOARD)


def _update_job(todo_id: int, raw: str | None) -> None:
    title = (raw or "").strip()
    try:
        updated = update_job(todo_id, title)
    except ValueError as err:
        show_error(str(err))
        return

    if not updated:
        show_error("Job no longer exists.")
        ui.navigate.to(ROUTE_DASHBOARD)
        return

    ui.navigate.to(route_job_detail(todo_id))
