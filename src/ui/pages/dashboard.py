from nicegui import ui

from domain.todos.facade import list_todos
from ui.constants import PAGE_TITLE, ROUTE_DASHBOARD
from ui.layout import build_page


def register_dashboard_page() -> None:
    @ui.page(ROUTE_DASHBOARD)
    def dashboard_page() -> None:
        ui.page_title(PAGE_TITLE)
        body = build_page(page="dashboard", title="Dashboard", subtitle="Overview of AI usage.")
        with body:
            render_dashboard_section()


def render_dashboard_section() -> None:
    todos = list_todos()
    ui.label(f"Total todos: {len(todos)}").classes("h2")
    ui.label("Queue monitoring is available in Monitor > Job Monitor.").classes("muted")
