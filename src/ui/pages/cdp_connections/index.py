from core.cdp_connections.facade import list_cdp_connections
from nicegui import ui

from ui.pages.cdp_connections.handlers import (
    close_create_panel,
    close_edit_panel,
    create_connection_from_form,
    delete_connection,
    find_connection,
    open_edit_panel,
    toggle_create_panel,
    update_connection_from_form,
)
from ui.pages.cdp_connections.ui_render import (
    render_chrome_debug_note,
    render_connections_table,
    render_create_panel,
    render_edit_panel,
    render_toolbar,
)


def render_cdp_connection_crud_section() -> None:
    state: dict[str, object] = {
        "show_create": False,
        "editing_id": None,
    }

    with ui.element("div").classes("card cdp-crud-card"):
        render_chrome_debug_note()

        @ui.refreshable
        def render_index() -> None:
            connections = list_cdp_connections()
            editing_connection = find_connection(connections, state["editing_id"])
            if editing_connection is None:
                state["editing_id"] = None

            render_toolbar(state, on_toggle_create=lambda: toggle_create_panel(state, render_index.refresh))

            if bool(state["show_create"]):
                render_create_panel(
                    on_create=lambda: create_connection_from_form("create", render_index.refresh, state),
                    on_cancel=lambda: close_create_panel(state, render_index.refresh),
                )

            render_connections_table(
                connections,
                on_edit=lambda connection_id: open_edit_panel(connection_id, state, render_index.refresh),
                on_delete=lambda connection_id: delete_connection(connection_id, render_index.refresh, state),
            )

            if editing_connection is not None:
                render_edit_panel(
                    editing_connection,
                    on_save=lambda: update_connection_from_form(
                        editing_connection.id,
                        f"edit-{editing_connection.id}",
                        render_index.refresh,
                        state,
                    ),
                    on_cancel=lambda: close_edit_panel(state, render_index.refresh),
                )

        render_index()
