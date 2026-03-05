from dataclasses import dataclass

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui

from ui.constants import PAGE_TITLE, ROUTE_DASHBOARD, ROUTE_MONITOR, ROUTE_ROOT, ROUTE_TODO
from ui.layout import build_page
from ui.pages.dashboard import render_dashboard_section
from ui.pages.monitor import _refresh_monitor_page, render_monitor_section
from ui.pages.todos import render_todo_crud_section

DEFAULT_VIEW = "todo"


@dataclass(frozen=True)
class ViewConfig:
    title: str
    subtitle: str


VIEW_CONFIGS = {
    "dashboard": ViewConfig(title="Dashboard", subtitle="Overview of AI usage."),
    "todo": ViewConfig(title="Todo CRUD", subtitle="Create, update, and manage todo items in one place."),
    "monitor": ViewConfig(title="Job Monitor", subtitle="Monitor queue jobs and worker operations in one place."),
}


def register_app_page() -> None:
    @ui.page(ROUTE_ROOT)
    def app_page(request: Request) -> None:
        ui.page_title(PAGE_TITLE)
        state = {"view": _parse_view(request)}

        @ui.refreshable
        def render_app() -> None:
            current_view = state["view"]
            view_config = VIEW_CONFIGS[current_view]
            body = build_page(
                page=current_view,
                title=view_config.title,
                subtitle=view_config.subtitle,
                on_navigate=lambda target: _change_view(target, state, render_app),
            )
            with body:
                _render_view_content(current_view)

        render_app()
        ui.timer(5.0, lambda: _poll_monitor_if_needed(state["view"]))

    @ui.page(ROUTE_DASHBOARD)
    def dashboard_alias() -> RedirectResponse:
        return RedirectResponse(f"{ROUTE_ROOT}?view=dashboard")

    @ui.page(ROUTE_TODO)
    def todo_alias() -> RedirectResponse:
        return RedirectResponse(f"{ROUTE_ROOT}?view=todo")

    @ui.page(ROUTE_MONITOR)
    def monitor_alias() -> RedirectResponse:
        return RedirectResponse(f"{ROUTE_ROOT}?view=monitor")


def _change_view(target: str, state: dict[str, str], render_app: object) -> None:
    if target not in VIEW_CONFIGS or state["view"] == target:
        return
    state["view"] = target
    ui.run_javascript(f"window.history.pushState({{}}, '', '/?view={target}')")
    refresh = getattr(render_app, "refresh", None)
    if callable(refresh):
        refresh()


def _parse_view(request: Request) -> str:
    requested = request.query_params.get("view", DEFAULT_VIEW).strip().lower()
    if requested in VIEW_CONFIGS:
        return requested
    return DEFAULT_VIEW


def _poll_monitor_if_needed(current_view: str) -> None:
    if current_view == "monitor":
        _refresh_monitor_page()


def _render_view_content(current_view: str) -> None:
    if current_view == "dashboard":
        render_dashboard_section()
        return
    if current_view == "monitor":
        render_monitor_section()
        return
    render_todo_crud_section()
