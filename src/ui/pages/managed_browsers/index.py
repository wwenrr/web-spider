from collections.abc import Callable
from core.managed_browsers.facade import list_managed_browsers
from nicegui import ui

from ui.pages.managed_browsers.handlers import (
    close_create_panel,
    close_edit_panel,
    create_browser_from_form,
    delete_browser,
    find_browser,
    open_edit_panel,
    start_browser,
    stop_browser,
    toggle_create_panel,
    update_browser_from_form,
)
from ui.pages.managed_browsers.ui_render import (
    render_browsers_table,
    render_create_panel,
    render_edit_panel,
    render_managed_browser_note,
    render_toolbar,
)

_refresh_managed_browsers: Callable[[], None] | None = None


def render_managed_browsers_section() -> None:
    state: dict[str, object] = {
        "show_create": False,
        "editing_id": None,
    }

    with ui.element("div").classes("card mb-crud-card"):
        render_managed_browser_note()

        @ui.refreshable
        def render_index() -> None:
            browsers = list_managed_browsers()
            editing_browser = find_browser(browsers, state["editing_id"])
            if editing_browser is None:
                state["editing_id"] = None

            render_toolbar(state, on_toggle_create=lambda: toggle_create_panel(state, render_index.refresh))

            if bool(state["show_create"]):
                render_create_panel(
                    on_create=lambda: create_browser_from_form("create", render_index.refresh, state),
                    on_cancel=lambda: close_create_panel(state, render_index.refresh),
                )

            render_browsers_table(
                browsers,
                on_edit=lambda browser_id: open_edit_panel(browser_id, state, render_index.refresh),
                on_delete=lambda browser_id: delete_browser(browser_id, render_index.refresh, state),
                on_start=lambda browser_id: start_browser(browser_id, render_index.refresh),
                on_stop=lambda browser_id: stop_browser(browser_id, render_index.refresh),
            )

            if editing_browser is not None:
                render_edit_panel(
                    editing_browser,
                    on_save=lambda: update_browser_from_form(
                        editing_browser.id,
                        f"edit-{editing_browser.id}",
                        render_index.refresh,
                        state,
                    ),
                    on_cancel=lambda: close_edit_panel(state, render_index.refresh),
                )

        global _refresh_managed_browsers
        _refresh_managed_browsers = render_index.refresh
        render_index()


def refresh_managed_browsers_section() -> None:
    if _refresh_managed_browsers is not None:
        _refresh_managed_browsers()
