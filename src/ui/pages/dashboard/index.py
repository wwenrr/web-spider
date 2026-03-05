from core.todos.facade import list_todos
from nicegui import ui


def render_dashboard_section() -> None:
    todos = list_todos()
    ui.label(f"Total todos: {len(todos)}").classes("h2")
    ui.label("Queue monitoring is available in Monitor > Job Monitor.").classes("muted")
