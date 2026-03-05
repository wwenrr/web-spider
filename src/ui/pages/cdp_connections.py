from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from html import escape
from typing import Final

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
    state: dict[str, object] = {
        "show_create": False,
        "editing_id": None,
    }

    with ui.element("div").classes("card cdp-crud-card"):
        _render_chrome_debug_note()

        @ui.refreshable
        def render_index() -> None:
            connections = list_cdp_connections()
            editing_connection = _find_connection(connections, state["editing_id"])
            if editing_connection is None:
                state["editing_id"] = None

            _render_toolbar(state, render_index.refresh)

            if bool(state["show_create"]):
                _render_create_panel(render_index.refresh, state)

            _render_connections_table(connections, refresh_index=render_index.refresh, state=state)

            if editing_connection is not None:
                _render_edit_panel(editing_connection, render_index.refresh, state)

        render_index()


def _render_toolbar(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    with ui.element("div").classes("cdp-toolbar"):
        _render_text("span", "Connection Index", "field-label cdp-toolbar-title")
        ui.element("div").classes("cdp-spacer")
        button_label = "Close Create" if bool(state["show_create"]) else "Create Connection"
        _render_native_button(
            label=button_label,
            classes="cdp-btn cdp-btn--primary",
            on_click=lambda _event=None: _toggle_create_panel(state, refresh_index),
        )


def _render_create_panel(refresh_index: Callable[[], None], state: dict[str, object]) -> None:
    with ui.element("div").classes("cdp-panel"):
        _render_text("span", "Create CDP Connection", "field-label cdp-panel-title")
        form_key = "create"
        _render_native_form(form_key=form_key, connection=None)

        async def on_create(_event: object | None = None) -> None:
            await _create_connection_from_form(form_key, refresh_index, state)

        with ui.element("div").classes("cdp-form-actions"):
            _render_native_button(
                label="Cancel",
                classes="cdp-btn cdp-btn--ghost",
                on_click=lambda _event=None: _close_create_panel(state, refresh_index),
            )
            _render_native_button(
                label="Create",
                classes="cdp-btn cdp-btn--primary",
                on_click=on_create,
            )


def _render_connections_table(
    connections: list[CdpConnection],
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    if not connections:
        _render_text("span", "No CDP connections yet. Click Create Connection to add one.", "todo-empty")
        return

    with ui.element("div").classes("cdp-table-wrap"):
        with ui.element("table").classes("cdp-table"):
            with ui.element("colgroup"):
                _render_table_col("14%")
                _render_table_col("11%")
                _render_table_col("8%")
                _render_table_col("11%")
                _render_table_col("20%")
                _render_table_col("12%")
                _render_table_col("12%")
                _render_table_col("12%")
            with ui.element("thead"):
                with ui.element("tr"):
                    _render_table_head("Name")
                    _render_table_head("Host")
                    _render_table_head("Port")
                    _render_table_head("Browser")
                    _render_table_head("Path")
                    _render_table_head("Status")
                    _render_table_head("Updated")
                    _render_table_head("Actions")

            with ui.element("tbody"):
                for connection in connections:
                    _render_table_row(connection, refresh_index, state)


def _render_table_row(
    connection: CdpConnection,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    with ui.element("tr"):
        _render_table_cell(connection.name)
        _render_table_cell(connection.host)
        _render_table_cell(str(connection.port), mono=True)
        _render_table_cell(connection.browser)
        _render_table_cell(connection.ws_path, mono=True)
        _render_status_cell(connection.is_active)
        _render_table_cell(_format_timestamp(connection.updated_at), mono=True)

        with ui.element("td").classes("cdp-td cdp-td-actions"):
            with ui.element("div").classes("cdp-actions-row"):
                _render_native_button(
                    label="Edit",
                    classes="cdp-btn cdp-btn--outline",
                    on_click=lambda _event=None, target_id=connection.id: _open_edit_panel(
                        target_id,
                        state,
                        refresh_index,
                    ),
                )
                _render_native_button(
                    label="Delete",
                    classes="cdp-btn cdp-btn--danger",
                    on_click=lambda _event=None, connection_id=connection.id: _delete_connection(
                        connection_id,
                        refresh_index,
                        state,
                    ),
                )


def _render_edit_panel(
    connection: CdpConnection,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    with ui.element("div").classes("cdp-panel"):
        _render_text("span", f"Edit Connection #{connection.id}", "field-label cdp-panel-title")
        form_key = f"edit-{connection.id}"
        _render_native_form(form_key=form_key, connection=connection)

        async def on_save(_event: object | None = None) -> None:
            await _update_connection_from_form(connection.id, form_key, refresh_index, state)

        with ui.element("div").classes("cdp-form-actions"):
            _render_native_button(
                label="Cancel",
                classes="cdp-btn cdp-btn--ghost",
                on_click=lambda _event=None: _close_edit_panel(state, refresh_index),
            )
            _render_native_button(
                label="Save",
                classes="cdp-btn cdp-btn--primary",
                on_click=on_save,
            )


def _render_chrome_debug_note() -> None:
    with ui.element("div").classes("cdp-note-box"):
        _render_text("span", "Run Chrome with remote debugging:", "cdp-note-title")
        _render_text(
            "code",
            'google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug-profile/"',
            "cdp-note-command",
        )


def _render_native_form(form_key: str, connection: CdpConnection | None) -> None:
    defaults = _defaults_from_connection(connection)
    checked = " checked" if defaults.is_active else ""

    with ui.element("div").classes("cdp-native-form").props(f'data-form-key="{form_key}"'):
        ui.html(
            f'<input id="{form_key}-name" class="cdp-native-input" type="text" '
            f'placeholder="Connection name" value="{escape(defaults.name)}">'
        )
        ui.html(
            f'<input id="{form_key}-host" class="cdp-native-input" type="text" '
            f'placeholder="127.0.0.1" value="{escape(defaults.host)}">'
        )
        ui.html(
            f'<input id="{form_key}-port" class="cdp-native-input" type="number" min="1" max="65535" '
            f'value="{defaults.port}">'
        )
        ui.html(
            f'<input id="{form_key}-browser" class="cdp-native-input" type="text" '
            f'placeholder="chrome" value="{escape(defaults.browser)}">'
        )
        ui.html(
            f'<input id="{form_key}-ws-path" class="cdp-native-input" type="text" '
            f'placeholder="/devtools/browser" value="{escape(defaults.ws_path)}">'
        )
        ui.html(
            f'<input id="{form_key}-username" class="cdp-native-input" type="text" '
            f'placeholder="Username (optional)" value="{escape(defaults.username or "")}">'
        )
        ui.html(
            f'<input id="{form_key}-password" class="cdp-native-input" type="password" '
            f'placeholder="Password (optional)" value="{escape(defaults.password or "")}">'
        )
        ui.html(
            f'<textarea id="{form_key}-notes" class="cdp-native-textarea" '
            f'placeholder="Notes (optional)">{escape(defaults.notes or "")}</textarea>'
        )
        ui.html(
            f'<label class="cdp-native-switch">'
            f'<input id="{form_key}-is-active" type="checkbox"{checked}>'
            f'<span>Active</span>'
            f"</label>"
        )


def _render_native_button(label: str, classes: str, on_click: Callable[..., object]) -> None:
    with ui.element("button").classes(classes).props("type=button").on("click", on_click):
        _render_text("span", label, "cdp-btn-label")


def _render_table_col(width: str) -> None:
    ui.element("col").style(f"width: {width};")


def _render_table_head(label: str) -> None:
    with ui.element("th").classes("cdp-th"):
        _render_text("span", label, "cdp-th-label")


def _render_table_cell(value: str, mono: bool = False) -> None:
    with ui.element("td").classes("cdp-td"):
        classes = "cdp-td-text cdp-td-text--mono" if mono else "cdp-td-text"
        _render_text("span", value, classes)


def _render_status_cell(is_active: bool) -> None:
    with ui.element("td").classes("cdp-td"):
        with ui.element("span").classes("cdp-status"):
            dot_classes = "cdp-status-dot cdp-status-dot--active" if is_active else "cdp-status-dot cdp-status-dot--inactive"
            ui.element("span").classes(dot_classes)
            _render_text("span", "Active" if is_active else "Inactive", "cdp-status-label")


def _render_text(tag: str, text: str, classes: str) -> None:
    with ui.element(tag).classes(classes):
        ui.html(escape(text))


def _format_timestamp(raw_time: object) -> str:
    if isinstance(raw_time, datetime):
        return raw_time.strftime("%d/%m/%Y")

    normalized = str(raw_time or "").strip()
    if normalized == "":
        return "-"

    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return normalized

    return parsed.strftime("%d/%m/%Y")


async def _create_connection_from_form(
    form_key: str,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    try:
        values = await _read_form_values(form_key)
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


async def _update_connection_from_form(
    connection_id: int,
    form_key: str,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    try:
        values = await _read_form_values(form_key)
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


def _delete_connection(connection_id: int, refresh_index: Callable[[], None], state: dict[str, object]) -> None:
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


async def _read_form_values(form_key: str) -> ConnectionFormValues:
    raw = await ui.run_javascript(
        f"""(() => {{
            const read = (id) => {{
                const element = document.getElementById(id);
                return element ? element.value : '';
            }};
            const readChecked = (id) => {{
                const element = document.getElementById(id);
                return Boolean(element && element.checked);
            }};
            return {{
                name: read('{form_key}-name'),
                host: read('{form_key}-host'),
                port: read('{form_key}-port'),
                browser: read('{form_key}-browser'),
                wsPath: read('{form_key}-ws-path'),
                username: read('{form_key}-username'),
                password: read('{form_key}-password'),
                notes: read('{form_key}-notes'),
                isActive: readChecked('{form_key}-is-active'),
            }};
        }})()"""
    )

    payload = raw if isinstance(raw, dict) else {}

    return ConnectionFormValues(
        name=str(payload.get("name", "")).strip(),
        host=str(payload.get("host", "")).strip(),
        port=_parse_port(payload.get("port")),
        browser=str(payload.get("browser", "")).strip(),
        ws_path=str(payload.get("wsPath", "")).strip(),
        username=_normalize_optional_text(payload.get("username")),
        password=_normalize_optional_text(payload.get("password")),
        is_active=bool(payload.get("isActive", False)),
        notes=_normalize_optional_text(payload.get("notes")),
    )


def _defaults_from_connection(connection: CdpConnection | None) -> ConnectionFormValues:
    if connection is None:
        return ConnectionFormValues(
            name="",
            host="",
            port=9222,
            browser="chrome",
            ws_path="/devtools/browser",
            username=None,
            password=None,
            is_active=True,
            notes=None,
        )

    return ConnectionFormValues(
        name=connection.name,
        host=connection.host,
        port=connection.port,
        browser=connection.browser,
        ws_path=connection.ws_path,
        username=connection.username,
        password=connection.password,
        is_active=connection.is_active,
        notes=connection.notes,
    )


def _parse_port(raw_port: object) -> int:
    as_text = str(raw_port or "").strip()
    if as_text == "":
        raise ValueError(PORT_PARSE_ERROR_MESSAGE)

    try:
        parsed_port = int(as_text)
    except ValueError as exc:
        raise ValueError(PORT_PARSE_ERROR_MESSAGE) from exc

    return parsed_port


def _normalize_optional_text(value: object) -> str | None:
    normalized = str(value or "").strip()
    if normalized == "":
        return None
    return normalized


def _toggle_create_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["show_create"] = not bool(state["show_create"])
    refresh_index()


def _close_create_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["show_create"] = False
    refresh_index()


def _open_edit_panel(connection_id: int, state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["editing_id"] = connection_id
    state["show_create"] = False
    refresh_index()


def _close_edit_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["editing_id"] = None
    refresh_index()


def _find_connection(connections: list[CdpConnection], raw_connection_id: object) -> CdpConnection | None:
    if not isinstance(raw_connection_id, int):
        return None

    for connection in connections:
        if connection.id == raw_connection_id:
            return connection

    return None
