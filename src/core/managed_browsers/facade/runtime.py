from core.managed_browsers.services import ManagedBrowserManager

_managed_browser_manager: ManagedBrowserManager | None = None


def configure_managed_browser_manager(managed_browser_manager: ManagedBrowserManager) -> None:
    global _managed_browser_manager
    _managed_browser_manager = managed_browser_manager


def get_managed_browser_manager() -> ManagedBrowserManager:
    if _managed_browser_manager is None:
        raise RuntimeError("ManagedBrowserManager is not configured")
    return _managed_browser_manager
