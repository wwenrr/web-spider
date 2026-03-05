from collections.abc import Callable
from datetime import datetime
from html import escape

from nicegui import ui

from infrastructure.models.cdp_connection import CdpConnection
from ui.pages.cdp_connections.form_values import defaults_from_connection


def render_chrome_debug_note() -> None:
    with ui.element("div").classes("cdp-note-box"):
        _render_text("span", "Run Chrome with remote debugging:", "cdp-note-title")
        _render_text(
            "code",
            'google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug-profile/"',
            "cdp-note-command",
        )


def render_toolbar(state: dict[str, object], on_toggle_create: Callable[[], None]) -> None:
    with ui.element("div").classes("cdp-toolbar"):
        _render_text("span", "Connection Index", "field-label cdp-toolbar-title")
        ui.element("div").classes("cdp-spacer")
        button_label = "Close Create" if bool(state["show_create"]) else "Create Connection"
        _render_native_button(
            label=button_label,
            classes="cdp-btn cdp-btn--primary",
            on_click=lambda _event=None: on_toggle_create(),
        )


def render_create_panel(
    on_create: Callable[[], object],
    on_cancel: Callable[[], object],
) -> None:
    with ui.element("div").classes("cdp-panel"):
        _render_text("span", "Create CDP Connection", "field-label cdp-panel-title")
        render_native_form(form_key="create", connection=None)
        with ui.element("div").classes("cdp-form-actions"):
            _render_native_button(
                label="Cancel",
                classes="cdp-btn cdp-btn--ghost",
                on_click=lambda _event=None: on_cancel(),
            )
            _render_native_button(
                label="Create",
                classes="cdp-btn cdp-btn--primary",
                on_click=lambda _event=None: on_create(),
            )


def render_edit_panel(
    connection: CdpConnection,
    on_save: Callable[[], object],
    on_cancel: Callable[[], object],
) -> None:
    with ui.element("div").classes("cdp-panel"):
        _render_text("span", f"Edit Connection #{connection.id}", "field-label cdp-panel-title")
        render_native_form(form_key=f"edit-{connection.id}", connection=connection)
        with ui.element("div").classes("cdp-form-actions"):
            _render_native_button(
                label="Cancel",
                classes="cdp-btn cdp-btn--ghost",
                on_click=lambda _event=None: on_cancel(),
            )
            _render_native_button(
                label="Save",
                classes="cdp-btn cdp-btn--primary",
                on_click=lambda _event=None: on_save(),
            )


def render_connections_table(
    connections: list[CdpConnection],
    on_edit: Callable[[int], None],
    on_delete: Callable[[int], None],
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
                    _render_table_row(connection, on_edit, on_delete)


def render_native_form(form_key: str, connection: CdpConnection | None) -> None:
    defaults = defaults_from_connection(connection)
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
            f"<span>Active</span>"
            f"</label>"
        )


def _render_table_row(
    connection: CdpConnection,
    on_edit: Callable[[int], None],
    on_delete: Callable[[int], None],
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
                    on_click=lambda _event=None, target_id=connection.id: on_edit(target_id),
                )
                _render_native_button(
                    label="Delete",
                    classes="cdp-btn cdp-btn--danger",
                    on_click=lambda _event=None, target_id=connection.id: on_delete(target_id),
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
