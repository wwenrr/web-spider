from core.managed_browsers.services import ManagedBrowserManager
from infrastructure.models.managed_browser import ManagedBrowser

from .runtime import get_managed_browser_manager


def list_managed_browsers() -> list[ManagedBrowser]:
    return _get_manager().list_browsers()


def create_managed_browser(
    name: str,
    browser_type: str,
    host: str,
    port: int,
    executable_path: str | None,
    user_data_dir: str,
    headless: bool,
    launch_args: str | None,
    is_active: bool,
    notes: str | None,
) -> None:
    _get_manager().create_browser(
        name,
        browser_type,
        host,
        port,
        executable_path,
        user_data_dir,
        headless,
        launch_args,
        is_active,
        notes,
    )


def update_managed_browser(
    browser_id: int,
    name: str,
    browser_type: str,
    host: str,
    port: int,
    executable_path: str | None,
    user_data_dir: str,
    headless: bool,
    launch_args: str | None,
    is_active: bool,
    notes: str | None,
) -> bool:
    return _get_manager().update_browser(
        browser_id,
        name,
        browser_type,
        host,
        port,
        executable_path,
        user_data_dir,
        headless,
        launch_args,
        is_active,
        notes,
    )


def delete_managed_browser(browser_id: int) -> bool:
    return _get_manager().delete_browser(browser_id)


def start_managed_browser(browser_id: int) -> ManagedBrowser:
    return _get_manager().start_browser(browser_id)


def stop_managed_browser(browser_id: int) -> ManagedBrowser:
    return _get_manager().stop_browser(browser_id)


def _get_manager() -> ManagedBrowserManager:
    return get_managed_browser_manager()
