from collections.abc import Callable

from core.cdp_connections.facade import create_cdp_connection, delete_cdp_connection, update_cdp_connection
from infrastructure.models.cdp_connection import CdpConnection
from ui.helpers import show_error, show_success
from ui.pages.cdp_connections.form_values import read_form_values


async def create_connection_from_form(
    form_key: str,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    try:
        values = await read_form_values(form_key)
        create_cdp_connection(
            values.name,
            values.host,
            values.port,
            values.browser,
            values.ws_path,
            values.username,
            values.password,
            values.is_active,
            values.notes,
        )
    except ValueError as err:
        show_error(str(err))
        return

    state["show_create"] = False
    refresh_index()
    show_success("CDP connection created")


async def update_connection_from_form(
    connection_id: int,
    form_key: str,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    try:
        values = await read_form_values(form_key)
        updated = update_cdp_connection(
            connection_id,
            values.name,
            values.host,
            values.port,
            values.browser,
            values.ws_path,
            values.username,
            values.password,
            values.is_active,
            values.notes,
        )
    except ValueError as err:
        show_error(str(err))
        return

    if not updated:
        state["editing_id"] = None
        refresh_index()
        show_error("Connection no longer exists.")
        return

    state["editing_id"] = None
    refresh_index()
    show_success("CDP connection updated")


def delete_connection(connection_id: int, refresh_index: Callable[[], None], state: dict[str, object]) -> None:
    deleted = delete_cdp_connection(connection_id)
    if not deleted:
        state["editing_id"] = None
        refresh_index()
        show_error("Connection no longer exists.")
        return

    if state["editing_id"] == connection_id:
        state["editing_id"] = None

    refresh_index()
    show_success("CDP connection deleted")


def toggle_create_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["show_create"] = not bool(state["show_create"])
    refresh_index()


def close_create_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["show_create"] = False
    refresh_index()


def open_edit_panel(connection_id: int, state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["editing_id"] = connection_id
    state["show_create"] = False
    refresh_index()


def close_edit_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["editing_id"] = None
    refresh_index()


def find_connection(connections: list[CdpConnection], raw_connection_id: object) -> CdpConnection | None:
    if not isinstance(raw_connection_id, int):
        return None

    for connection in connections:
        if connection.id == raw_connection_id:
            return connection
    return None
