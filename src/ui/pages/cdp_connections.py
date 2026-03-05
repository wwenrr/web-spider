from collections.abc import Callable
from dataclasses import dataclass
from typing import Final, cast

from nicegui import ui

from domain.cdp_connections.facade import (
    create_cdp_connection,
    delete_cdp_connection,
    list_cdp_connections,
    update_cdp_connection,
)
from models.cdp_connection import CdpConnection
from ui.helpers import show_error, show_success

PORT_PARSE_ERROR_MESSAGE: Final[str] = "Port phải là số nguyên hợp lệ"


@dataclass(frozen=True)
class ConnectionFormValues:
    name: str
    host: str
    port: int
    browser: str
    ws_path: str
    username: str | None
    password: str | None
    is_active: bool
    notes: str | None


def render_cdp_connection_crud_section() -> None:
    with ui.card().classes("card cdp-crud-card"):
        ui.label("Create CDP Connection").classes("field-label")
        create_fields = _render_form_fields()

        with ui.row().classes("cdp-create-actions"):
            ui.button(
                "Add Connection",
                on_click=lambda: _create_connection(
                    create_fields,
                    refresh_list=render_connections.refresh,
                    clear_form=lambda: _reset_form_fields(create_fields),
                ),
            ).props("unelevated no-caps size=sm").classes("btn-primary cdp-submit-btn")

        @ui.refreshable
        def render_connections() -> None:
            connections = list_cdp_connections()
            if not connections:
                ui.label("No CDP connections yet. Add one above to get started.").classes("todo-empty")
                return

            with ui.column().classes("cdp-list"):
                for connection in connections:
                    _render_connection_row(connection, refresh_list=render_connections.refresh)

        render_connections()


def _render_connection_row(connection: CdpConnection, refresh_list: Callable[[], None]) -> None:
    with ui.element("div").classes("cdp-row"):
        with ui.column().classes("gap-0 cdp-row-header"):
            ui.label(connection.name).classes("todo-title")
            ui.label(f"{connection.host}:{connection.port} • {connection.browser}").classes("todo-id")
            ui.label(connection.ws_path).classes("todo-id")

        edit_fields = _render_form_fields(connection)

        with ui.row().classes("cdp-actions-row"):
            ui.button(
                "Save",
                on_click=lambda connection_id=connection.id: _update_connection(
                    connection_id,
                    edit_fields,
                    refresh_list,
                ),
            ).props("unelevated no-caps size=sm").classes("btn-primary")
            ui.button(
                "Delete",
                on_click=lambda connection_id=connection.id: _delete_connection(connection_id, refresh_list),
            ).props("flat no-caps color=red-7 size=sm")


def _create_connection(
    fields: dict[str, object],
    refresh_list: Callable[[], None],
    clear_form: Callable[[], None],
) -> None:
    try:
        values = _collect_form_values(fields)
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

    clear_form()
    refresh_list()
    show_success("CDP connection created")


def _update_connection(connection_id: int, fields: dict[str, object], refresh_list: Callable[[], None]) -> None:
    try:
        values = _collect_form_values(fields)
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
        show_error("Connection no longer exists.")
        refresh_list()
        return

    refresh_list()
    show_success("CDP connection updated")


def _delete_connection(connection_id: int, refresh_list: Callable[[], None]) -> None:
    deleted = delete_cdp_connection(connection_id)
    if not deleted:
        show_error("Connection no longer exists.")
        refresh_list()
        return

    refresh_list()
    show_success("CDP connection deleted")


def _render_form_fields(connection: CdpConnection | None = None) -> dict[str, object]:
    with ui.column().classes("cdp-form-grid w-full"):
        name = ui.input(value=connection.name if connection else "", placeholder="Connection name").classes("cdp-input")
        name.props("outlined dense").classes("w-full").style("width: 100%")

        host = ui.input(value=connection.host if connection else "", placeholder="127.0.0.1").classes("cdp-input")
        host.props("outlined dense").classes("w-full").style("width: 100%")

        port = ui.number(value=connection.port if connection else 9222, min=1, max=65535).classes("cdp-input")
        port.props("outlined dense").classes("w-full").style("width: 100%")

        browser = ui.input(value=connection.browser if connection else "chrome", placeholder="chrome").classes("cdp-input")
        browser.props("outlined dense").classes("w-full").style("width: 100%")

        ws_path = ui.input(
            value=connection.ws_path if connection else "/devtools/browser",
            placeholder="/devtools/browser",
        ).classes("cdp-input")
        ws_path.props("outlined dense").classes("w-full").style("width: 100%")

        username = ui.input(
            value=connection.username or "" if connection else "",
            placeholder="Username (optional)",
        ).classes("cdp-input")
        username.props("outlined dense").classes("w-full").style("width: 100%")

        password = ui.input(
            value=connection.password or "" if connection else "",
            placeholder="Password (optional)",
            password=True,
        ).classes("cdp-input")
        password.props("outlined dense").classes("w-full").style("width: 100%")

        notes = ui.textarea(value=connection.notes or "" if connection else "", placeholder="Notes (optional)").classes(
            "cdp-textarea w-full"
        )
        notes.props("outlined dense").style("width: 100%")

        is_active = ui.switch("Active", value=connection.is_active if connection else True).classes("cdp-switch w-full")

    return {
        "name": name,
        "host": host,
        "port": port,
        "browser": browser,
        "ws_path": ws_path,
        "username": username,
        "password": password,
        "notes": notes,
        "is_active": is_active,
    }


def _collect_form_values(fields: dict[str, object]) -> ConnectionFormValues:
    return ConnectionFormValues(
        name=_string_value(fields["name"]),
        host=_string_value(fields["host"]),
        port=_port_value(fields["port"]),
        browser=_string_value(fields["browser"]),
        ws_path=_string_value(fields["ws_path"]),
        username=_optional_string_value(fields["username"]),
        password=_optional_string_value(fields["password"]),
        is_active=_bool_value(fields["is_active"]),
        notes=_optional_string_value(fields["notes"]),
    )


def _reset_form_fields(fields: dict[str, object]) -> None:
    _set_component_value(fields["name"], "")
    _set_component_value(fields["host"], "")
    _set_component_value(fields["port"], 9222)
    _set_component_value(fields["browser"], "chrome")
    _set_component_value(fields["ws_path"], "/devtools/browser")
    _set_component_value(fields["username"], "")
    _set_component_value(fields["password"], "")
    _set_component_value(fields["notes"], "")
    _set_component_value(fields["is_active"], True)


def _string_value(component: object) -> str:
    return str(_get_component_value(component) or "").strip()


def _optional_string_value(component: object) -> str | None:
    normalized = _string_value(component)
    if normalized == "":
        return None
    return normalized


def _port_value(component: object) -> int:
    raw_value = _get_component_value(component)
    if raw_value is None:
        raise ValueError(PORT_PARSE_ERROR_MESSAGE)

    if isinstance(raw_value, bool):
        raise ValueError(PORT_PARSE_ERROR_MESSAGE)

    if isinstance(raw_value, int):
        return raw_value

    if isinstance(raw_value, float):
        if raw_value.is_integer():
            return int(raw_value)
        raise ValueError(PORT_PARSE_ERROR_MESSAGE)

    as_text = str(raw_value).strip()
    if as_text == "":
        raise ValueError(PORT_PARSE_ERROR_MESSAGE)

    try:
        return int(as_text)
    except ValueError as exc:
        raise ValueError(PORT_PARSE_ERROR_MESSAGE) from exc


def _bool_value(component: object) -> bool:
    return bool(_get_component_value(component))


def _get_component_value(component: object) -> object:
    return cast(object, getattr(component, "value", None))


def _set_component_value(component: object, value: object) -> None:
    setattr(component, "value", value)
