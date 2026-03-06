from core.managed_browsers.interfaces import IManagedBrowserRepository
from infrastructure.helpers.managed_browser_runtime import ManagedBrowserRuntime
from infrastructure.models.managed_browser import ManagedBrowser


class ManagedBrowserManager:
    def __init__(self, repository: IManagedBrowserRepository, runtime: ManagedBrowserRuntime) -> None:
        self._repository = repository
        self._runtime = runtime

    def list_browsers(self) -> list[ManagedBrowser]:
        return self._runtime.list_browsers()

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
    ) -> None:
        self._repository.create_browser(
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
    ) -> bool:
        return self._repository.update_browser(
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

    def delete_browser(self, browser_id: int) -> bool:
        return self._repository.delete_browser(browser_id)

    def start_browser(self, browser_id: int) -> ManagedBrowser:
        return self._runtime.start_browser(browser_id)

    def stop_browser(self, browser_id: int) -> ManagedBrowser:
        return self._runtime.stop_browser(browser_id)
