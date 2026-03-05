from collections.abc import Callable

from fastapi.responses import RedirectResponse
from nicegui import ui

from domain.todos.facade import create_todo, delete_todo, list_todos, toggle_todo, update_todo
from models.todo import Todo
from ui.components.badges import render_status_badge
from ui.constants import PAGE_TITLE, ROUTE_ROOT, ROUTE_TODO
from ui.helpers import show_error, show_success
from ui.layout import build_page


def register_todos_page() -> None:
    @ui.page(ROUTE_ROOT)
    def root_page() -> RedirectResponse:
        return RedirectResponse(ROUTE_TODO)

    @ui.page(ROUTE_TODO)
    def todos_page() -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(
            page="todo",
            title="Todo CRUD",
            subtitle="Create, update, and manage todo items in one place.",
        )
        with body:
            render_todo_crud_section()


def render_todo_crud_section() -> None:
    with ui.card().classes("card todo-crud-card"):
        ui.label("Create Todo").classes("field-label")
        with ui.row().classes("todo-create-row"):
            create_field = ui.input(
                placeholder="e.g. Review crawler output and publish report",
            ).classes("todo-input")
            create_field.props("outlined dense")
            ui.button(
                "Add Todo",
                on_click=lambda: _create_todo(
                    create_field.value,
                    refresh_list=render_todo_list.refresh,
                    clear_input=lambda: setattr(create_field, "value", ""),
                ),
            ).props(
                "unelevated no-caps size=sm"
            ).classes("btn-primary todo-add-btn")

        @ui.refreshable
        def render_todo_list() -> None:
            todos = list_todos()
            if not todos:
                ui.label("No todo items yet. Add one above to get started.").classes("todo-empty")
                return

            with ui.column().classes("todo-list"):
                for todo in todos:
                    _render_todo_row(todo, refresh_list=render_todo_list.refresh)

        render_todo_list()


def _render_todo_row(todo: Todo, refresh_list: Callable[[], None]) -> None:
    with ui.element("div").classes("todo-row"):
        with ui.column().classes("gap-0 todo-title-block"):
            ui.label(todo.title).classes("todo-title")
            with ui.row().classes("todo-meta-row"):
                render_status_badge(todo.is_done)
                ui.label(f"ID #{todo.id}").classes("todo-id")

        edit_field = ui.input(value=todo.title, placeholder="Update todo title").classes("todo-input")
        edit_field.props("outlined dense")

        with ui.row().classes("todo-actions-row"):
            ui.button(
                "Save",
                on_click=lambda todo_id=todo.id: _update_todo(todo_id, edit_field.value, refresh_list),
            ).props("unelevated no-caps size=sm").classes("btn-primary")
            ui.button("Toggle", on_click=lambda todo_id=todo.id: _toggle_todo(todo_id, refresh_list)).props(
                "outline no-caps size=sm"
            )
            ui.button("Delete", on_click=lambda todo_id=todo.id: _delete_todo(todo_id, refresh_list)).props(
                "flat no-caps color=red-7 size=sm"
            )


def _create_todo(raw_title: str | None, refresh_list: Callable[[], None], clear_input: Callable[[], None]) -> None:
    title = (raw_title or "").strip()
    try:
        create_todo(title)
    except ValueError as err:
        show_error(str(err))
        return

    clear_input()
    refresh_list()
    show_success("Todo created")


def _update_todo(todo_id: int, raw_title: str | None, refresh_list: Callable[[], None]) -> None:
    title = (raw_title or "").strip()
    try:
        updated = update_todo(todo_id, title)
    except ValueError as err:
        show_error(str(err))
        return

    if not updated:
        show_error("Todo no longer exists.")
        refresh_list()
        return

    refresh_list()
    show_success("Todo updated")


def _toggle_todo(todo_id: int, refresh_list: Callable[[], None]) -> None:
    toggle_todo(todo_id)
    refresh_list()
    show_success("Todo status updated")


def _delete_todo(todo_id: int, refresh_list: Callable[[], None]) -> None:
    deleted = delete_todo(todo_id)
    if not deleted:
        show_error("Todo no longer exists.")
        refresh_list()
        return

    refresh_list()
    show_success("Todo deleted")
