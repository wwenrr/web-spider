from collections.abc import Callable
from datetime import datetime
from html import escape

from nicegui import ui

from infrastructure.models.managed_browser import ManagedBrowser, ManagedBrowserStatus
from ui.pages.managed_browsers.form_values import defaults_from_browser


def render_managed_browser_note() -> None:
    with ui.element("div").classes("mb-note-box"):
        _render_text("span", "Fallback order", "mb-note-title")
        _render_text(
            "span",
            "Crawlers attach to an active external CDP first. If none is available, the app will reuse an active managed browser over local CDP instead of launching a new browser per task.",
            "mb-note-copy",
        )


def render_toolbar(state: dict[str, object], on_toggle_create: Callable[[], None]) -> None:
    with ui.element("div").classes("mb-toolbar"):
        _render_text("span", "Managed Browser Index", "field-label mb-toolbar-title")
        ui.element("div").classes("mb-spacer")
        button_label = "Close Create" if bool(state["show_create"]) else "Create Browser"
        _render_native_button(button_label, "mb-btn mb-btn--primary", lambda _event=None: on_toggle_create())


def render_create_panel(on_create: Callable[[], object], on_cancel: Callable[[], object]) -> None:
    with ui.element("div").classes("mb-panel"):
        _render_text("span", "Create Managed Browser", "field-label mb-panel-title")
        render_native_form(form_key="create", browser=None)
        with ui.element("div").classes("mb-form-actions"):
            _render_native_button("Cancel", "mb-btn mb-btn--ghost", lambda _event=None: on_cancel())
            _render_native_button("Create", "mb-btn mb-btn--primary", lambda _event=None: on_create())


def render_edit_panel(browser: ManagedBrowser, on_save: Callable[[], object], on_cancel: Callable[[], object]) -> None:
    with ui.element("div").classes("mb-panel"):
        _render_text("span", f"Edit Browser #{browser.id}", "field-label mb-panel-title")
        render_native_form(form_key=f"edit-{browser.id}", browser=browser)
        with ui.element("div").classes("mb-form-actions"):
            _render_native_button("Cancel", "mb-btn mb-btn--ghost", lambda _event=None: on_cancel())
            _render_native_button("Save", "mb-btn mb-btn--primary", lambda _event=None: on_save())


def render_browsers_table(
    browsers: list[ManagedBrowser],
    on_edit: Callable[[int], None],
    on_delete: Callable[[int], None],
    on_start: Callable[[int], None],
    on_stop: Callable[[int], None],
) -> None:
    if not browsers:
        _render_text("span", "No managed browsers yet. Create one to reuse local fallback sessions.", "todo-empty")
        return

    with ui.element("div").classes("mb-table-wrap"):
        with ui.element("table").classes("mb-table"):
            with ui.element("colgroup"):
                for width in ("16%", "8%", "9%", "8%", "10%", "12%", "11%", "10%", "16%"):
                    _render_table_col(width)
            with ui.element("thead"):
                with ui.element("tr"):
                    _render_table_head("Name")
                    _render_table_head("Browser")
                    _render_table_head("Endpoint")
                    _render_table_head("Status")
                    _render_table_head("Profile")
                    _render_table_head("Mode")
                    _render_table_head("Last Seen")
                    _render_table_head("Active")
                    _render_table_head("Actions")
            with ui.element("tbody"):
                for browser in browsers:
                    _render_table_row(browser, on_edit, on_delete, on_start, on_stop)


def render_native_form(form_key: str, browser: ManagedBrowser | None) -> None:
    defaults = defaults_from_browser(browser)
    headless_checked = " checked" if defaults.headless else ""
    active_checked = " checked" if defaults.is_active else ""
    with ui.element("div").classes("mb-native-form").props(f'data-form-key="{form_key}"'):
        ui.html(
            f'<input id="{form_key}-name" class="mb-native-input" type="text" '
            f'placeholder="Optional name, auto-generated if empty" value="{escape(defaults.name)}">'
        )
        ui.html(
            f'<input id="{form_key}-browser-type" class="mb-native-input" type="text" '
            f'placeholder="chrome" value="{escape(defaults.browser_type)}">'
        )
        ui.html(
            f'<input id="{form_key}-host" class="mb-native-input" type="text" '
            f'placeholder="127.0.0.1" value="{escape(defaults.host)}">'
        )
        ui.html(
            f'<input id="{form_key}-port" class="mb-native-input" type="number" min="1" max="65535" '
            f'value="{defaults.port}">'
        )
        ui.html(
            f'<input id="{form_key}-executable-path" class="mb-native-input" type="text" '
            f'placeholder="/usr/bin/google-chrome (optional)" value="{escape(defaults.executable_path or "")}">'
        )
        ui.html(
            f'<input id="{form_key}-user-data-dir" class="mb-native-input" type="text" '
            f'placeholder="/tmp/web-spider-managed-browser" value="{escape(defaults.user_data_dir)}">'
        )
        ui.html(
            f'<textarea id="{form_key}-launch-args" class="mb-native-textarea" '
            f'placeholder="Extra CLI args (optional)">{escape(defaults.launch_args or "")}</textarea>'
        )
        ui.html(
            f'<textarea id="{form_key}-notes" class="mb-native-textarea" '
            f'placeholder="Notes (optional)">{escape(defaults.notes or "")}</textarea>'
        )
        ui.html(
            f'<div class="mb-toggle-row">'
            f'<label class="mb-native-switch"><input id="{form_key}-headless" type="checkbox"{headless_checked}><span>Headless</span></label>'
            f'<label class="mb-native-switch"><input id="{form_key}-is-active" type="checkbox"{active_checked}><span>Active fallback</span></label>'
            f'</div>'
        )


def _render_table_row(
    browser: ManagedBrowser,
    on_edit: Callable[[int], None],
    on_delete: Callable[[int], None],
    on_start: Callable[[int], None],
    on_stop: Callable[[int], None],
) -> None:
    with ui.element("tr"):
        with ui.element("td").classes("mb-td"):
            _render_text("span", browser.name, "mb-td-text")
            _render_text("span", browser.notes or "-", "mb-td-subtext")
        _render_table_cell(browser.browser_type)
        _render_table_cell(f"{browser.host}:{browser.port}", mono=True)
        _render_status_cell(browser)
        _render_table_cell(browser.user_data_dir, mono=True)
        _render_table_cell("Headless" if browser.headless else "Visible")
        _render_table_cell(_format_timestamp(browser.last_seen_at), mono=True)
        _render_active_cell(browser.is_active)
        with ui.element("td").classes("mb-td mb-td-actions"):
            with ui.element("div").classes("mb-actions-row"):
                if browser.status == ManagedBrowserStatus.RUNNING.value:
                    _render_native_button("Stop", "mb-btn mb-btn--outline", lambda _event=None, target_id=browser.id: on_stop(target_id))
                else:
                    _render_native_button("Start", "mb-btn mb-btn--outline", lambda _event=None, target_id=browser.id: on_start(target_id))
                _render_native_button("Edit", "mb-btn mb-btn--ghost", lambda _event=None, target_id=browser.id: on_edit(target_id))
                _render_native_button("Delete", "mb-btn mb-btn--danger", lambda _event=None, target_id=browser.id: on_delete(target_id))


def _render_native_button(label: str, classes: str, on_click: Callable[..., object]) -> None:
    with ui.element("button").classes(classes).props("type=button").on("click", on_click):
        _render_text("span", label, "mb-btn-label")


def _render_table_col(width: str) -> None:
    ui.element("col").style(f"width: {width};")


def _render_table_head(label: str) -> None:
    with ui.element("th").classes("mb-th"):
        _render_text("span", label, "mb-th-label")


def _render_table_cell(value: str, mono: bool = False) -> None:
    with ui.element("td").classes("mb-td"):
        classes = "mb-td-text mb-td-text--mono" if mono else "mb-td-text"
        _render_text("span", value, classes)


def _render_status_cell(browser: ManagedBrowser) -> None:
    with ui.element("td").classes("mb-td"):
        with ui.element("span").classes("mb-status"):
            with ui.element("span").classes("mb-status-row"):
                ui.element("span").classes(f"mb-status-dot mb-status-dot--{browser.status}")
                _render_text("span", browser.status.capitalize(), "mb-status-label")
            if browser.error_message:
                _render_text("span", browser.error_message, "mb-status-error")


def _render_active_cell(is_active: bool) -> None:
    with ui.element("td").classes("mb-td"):
        with ui.element("span").classes("mb-active-pill" + (" mb-active-pill--on" if is_active else "")):
            _render_text("span", "Active" if is_active else "Idle", "mb-active-pill-label")


def _render_text(tag: str, text: str, classes: str) -> None:
    with ui.element(tag).classes(classes):
        ui.html(escape(text))


def _format_timestamp(raw_time: object) -> str:
    if isinstance(raw_time, datetime):
        return raw_time.strftime("%d/%m/%Y %H:%M")
    normalized = str(raw_time or "").strip()
    if normalized == "":
        return "-"
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return normalized
    return parsed.strftime("%d/%m/%Y %H:%M")
