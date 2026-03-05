from collections.abc import Callable

from nicegui import ui

from models.todo import Todo
from ui.components.badges import render_status_badge
from ui.pages.todos.actions import handle_delete_todo, handle_toggle_todo, handle_update_todo


def render_todo_row(todo: Todo, refresh_list: Callable[[], None]) -> None:
    with ui.element("div").classes("todo-row"):
        with ui.element("div").classes("todo-row-header"):
            render_status_badge(todo.is_done)
            ui.label(todo.title).classes("todo-title")
            ui.label(f"#{todo.id}").classes("todo-id")

        with ui.element("div").classes("todo-row-body"):
            edit_field = ui.input(value=todo.title, placeholder="Update title…").classes("todo-input")
            edit_field.props("outlined dense")

            done_icon = "undo" if todo.is_done else "check"
            done_tip = "Mark pending" if todo.is_done else "Mark done"
            ui.button(
                icon=done_icon,
                on_click=lambda todo_id=todo.id: handle_toggle_todo(todo_id, refresh_list),
            ).props("flat dense size=sm").classes("todo-btn-icon todo-btn-toggle").tooltip(done_tip)
            ui.button(
                "Save",
                on_click=lambda todo_id=todo.id: handle_update_todo(todo_id, edit_field.value, refresh_list),
            ).props("unelevated no-caps size=sm").classes("btn-primary todo-save-btn")
            ui.button(
                icon="close",
                on_click=lambda todo_id=todo.id: handle_delete_todo(todo_id, refresh_list),
            ).props("flat dense size=sm").classes("todo-btn-icon todo-btn-delete").tooltip("Delete")
