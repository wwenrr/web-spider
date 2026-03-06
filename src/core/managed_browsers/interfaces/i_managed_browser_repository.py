from typing import Protocol

from infrastructure.models.managed_browser import ManagedBrowser


class IManagedBrowserRepository(Protocol):
    def list_browsers(self) -> list[ManagedBrowser]: ...

    def get_browser(self, browser_id: int) -> ManagedBrowser | None: ...

    def get_active_browser(self) -> ManagedBrowser | None: ...

    def ensure_default_active_browser(self, *, headless: bool) -> ManagedBrowser: ...

    def create_browser(
        self,
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
    ) -> None: ...

    def update_browser(
        self,
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
    ) -> bool: ...

    def delete_browser(self, browser_id: int) -> bool: ...
