from fastapi.responses import RedirectResponse
from nicegui import ui

from domain.todos.facade import list_todos
from ui.constants import PAGE_TITLE, ROUTE_ROOT, ROUTE_TODO
from ui.layout import build_page
from ui.pages.todos.actions import handle_create_todo
from ui.pages.todos.row import render_todo_row


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
        with ui.element("div").classes("todo-create-row"):
            create_field = ui.input(
                placeholder="e.g. Review crawler output and publish report",
            ).classes("todo-input")
            create_field.props("outlined dense")
            ui.button(
                "Add Todo",
                on_click=lambda: handle_create_todo(
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

            with ui.element("div").classes("todo-list"):
                for todo in todos:
                    render_todo_row(todo, refresh_list=render_todo_list.refresh)

        render_todo_list()
