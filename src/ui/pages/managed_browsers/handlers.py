from collections.abc import Callable

from core.managed_browsers.facade import (
    create_managed_browser,
    delete_managed_browser,
    start_managed_browser,
    stop_managed_browser,
    update_managed_browser,
)
from infrastructure.models.managed_browser import ManagedBrowser
from ui.helpers import show_error, show_success
from ui.pages.managed_browsers.form_values import read_form_values


async def create_browser_from_form(
    form_key: str,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    try:
        values = await read_form_values(form_key)
        create_managed_browser(
            values.name,
            values.browser_type,
            values.host,
            values.port,
            values.executable_path,
            values.user_data_dir,
            values.headless,
            values.launch_args,
            values.is_active,
            values.notes,
        )
    except ValueError as err:
        show_error(str(err))
        return

    state["show_create"] = False
    refresh_index()
    show_success("Managed browser created.")


async def update_browser_from_form(
    browser_id: int,
    form_key: str,
    refresh_index: Callable[[], None],
    state: dict[str, object],
) -> None:
    try:
        values = await read_form_values(form_key)
        updated = update_managed_browser(
            browser_id,
            values.name,
            values.browser_type,
            values.host,
            values.port,
            values.executable_path,
            values.user_data_dir,
            values.headless,
            values.launch_args,
            values.is_active,
            values.notes,
        )
    except ValueError as err:
        show_error(str(err))
        return

    if not updated:
        state["editing_id"] = None
        refresh_index()
        show_error("Managed browser no longer exists.")
        return

    state["editing_id"] = None
    refresh_index()
    show_success("Managed browser updated.")


def delete_browser(browser_id: int, refresh_index: Callable[[], None], state: dict[str, object]) -> None:
    try:
        deleted = delete_managed_browser(browser_id)
    except ValueError as err:
        show_error(str(err))
        return

    if not deleted:
        state["editing_id"] = None
        refresh_index()
        show_error("Managed browser no longer exists.")
        return

    if state["editing_id"] == browser_id:
        state["editing_id"] = None

    refresh_index()
    show_success("Managed browser deleted.")


def start_browser(browser_id: int, refresh_index: Callable[[], None]) -> None:
    try:
        start_managed_browser(browser_id)
    except ValueError as err:
        show_error(str(err))
        return
    except RuntimeError as err:
        show_error(str(err))
        return

    refresh_index()
    show_success("Managed browser started.")


def stop_browser(browser_id: int, refresh_index: Callable[[], None]) -> None:
    try:
        stop_managed_browser(browser_id)
    except ValueError as err:
        show_error(str(err))
        return

    refresh_index()
    show_success("Managed browser stopped.")


def toggle_create_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["show_create"] = not bool(state["show_create"])
    refresh_index()


def close_create_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["show_create"] = False
    refresh_index()


def open_edit_panel(browser_id: int, state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["editing_id"] = browser_id
    state["show_create"] = False
    refresh_index()


def close_edit_panel(state: dict[str, object], refresh_index: Callable[[], None]) -> None:
    state["editing_id"] = None
    refresh_index()


def find_browser(browsers: list[ManagedBrowser], raw_browser_id: object) -> ManagedBrowser | None:
    if not isinstance(raw_browser_id, int):
        return None

    for browser in browsers:
        if browser.id == raw_browser_id:
            return browser
    return None
