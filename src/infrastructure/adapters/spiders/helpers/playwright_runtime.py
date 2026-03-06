from dataclasses import dataclass
from threading import Lock
from urllib.parse import quote, urlsplit, urlunsplit

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from infrastructure.helpers.managed_browser_runtime import get_managed_browser_runtime
from infrastructure.models.cdp_connection import CdpConnection
from infrastructure.repositories.cdp_connection import get_cdp_connection_repository

DEFAULT_LOCALE = "ja-JP"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class PlaywrightPageSession:
    page: Page
    source: str
    _owned_context: BrowserContext | None

    def close(self) -> None:
        try:
            self.page.close()
        finally:
            if self._owned_context is not None:
                self._owned_context.close()


class SharedPlaywrightRuntime:
    def __init__(self) -> None:
        self._lock = Lock()
        self._playwright: Playwright | None = None
        self._cdp_browser: Browser | None = None
        self._browser_cache_key: str | None = None

    def open_page(self, *, headless: bool) -> PlaywrightPageSession:
        with self._lock:
            external_cdp_session = self._try_open_external_cdp_page()
            if external_cdp_session is not None:
                return external_cdp_session
            managed_browser_session = self._try_open_managed_browser_page(headless=headless)
            if managed_browser_session is not None:
                return managed_browser_session
            raise RuntimeError("No active external CDP connection or managed browser is available.")

    def _try_open_external_cdp_page(self) -> PlaywrightPageSession | None:
        active_connection = _get_active_cdp_connection()
        if active_connection is None:
            self._disconnect_cached_browser(except_cache_key=None)
            return None

        cache_key = f"cdp:{active_connection.id}"
        browser = self._resolve_cdp_browser(cache_key=cache_key, endpoint_url=_build_cdp_endpoint(active_connection))
        if browser is None:
            return None
        return _open_browser_page(browser=browser, source="cdp")

    def _try_open_managed_browser_page(self, *, headless: bool) -> PlaywrightPageSession | None:
        runtime = get_managed_browser_runtime()
        browser_config = runtime.ensure_active_browser(headless=headless)
        cache_key = f"managed:{browser_config.id}"
        browser = self._resolve_cdp_browser(cache_key=cache_key, endpoint_url=runtime.endpoint_for(browser_config))
        if browser is None:
            return None
        return _open_browser_page(browser=browser, source="managed")

    def _resolve_cdp_browser(self, *, cache_key: str, endpoint_url: str) -> Browser | None:
        if self._cdp_browser is not None and self._cdp_browser.is_connected() and self._browser_cache_key == cache_key:
            return self._cdp_browser

        self._disconnect_cached_browser(except_cache_key=cache_key)
        try:
            self._cdp_browser = self._get_playwright().chromium.connect_over_cdp(endpoint_url=endpoint_url)
        except Exception:
            self._cdp_browser = None
            self._browser_cache_key = None
            return None

        self._browser_cache_key = cache_key
        return self._cdp_browser

    def _get_playwright(self) -> Playwright:
        if self._playwright is None:
            self._playwright = sync_playwright().start()
        return self._playwright

    def _disconnect_cached_browser(self, *, except_cache_key: str | None) -> None:
        if self._cdp_browser is None:
            self._browser_cache_key = except_cache_key if self._browser_cache_key == except_cache_key else None
            return
        if except_cache_key is not None and self._browser_cache_key == except_cache_key and self._cdp_browser.is_connected():
            return
        try:
            self._cdp_browser.close()
        except Exception:
            pass
        finally:
            self._cdp_browser = None
            self._browser_cache_key = None


_shared_playwright_runtime: SharedPlaywrightRuntime | None = None


def get_shared_playwright_runtime() -> SharedPlaywrightRuntime:
    global _shared_playwright_runtime
    if _shared_playwright_runtime is None:
        _shared_playwright_runtime = SharedPlaywrightRuntime()
    return _shared_playwright_runtime


def _get_active_cdp_connection() -> CdpConnection | None:
    repository = get_cdp_connection_repository()
    for connection in repository.list_connections():
        if connection.is_active:
            return connection
    return None


def _build_cdp_endpoint(connection: CdpConnection) -> str:
    normalized_host = connection.host.strip()
    normalized_path = _normalize_cdp_path(connection.ws_path)
    if "://" not in normalized_host:
        scheme = "ws" if _is_full_browser_ws_path(normalized_path) else "http"
        return urlunsplit(
            (
                scheme,
                _build_netloc(
                    host=normalized_host,
                    port=connection.port,
                    username=connection.username,
                    password=connection.password,
                ),
                normalized_path if scheme == "ws" else "",
                "",
                "",
            )
        )

    host_parts = urlsplit(normalized_host)
    scheme = host_parts.scheme or "http"
    host = host_parts.hostname or normalized_host
    port = host_parts.port or connection.port
    username = host_parts.username or connection.username
    password = host_parts.password or connection.password
    normalized_scheme = _normalize_cdp_scheme(scheme=scheme, path=normalized_path)
    return urlunsplit(
        (
            normalized_scheme,
            _build_netloc(host=host, port=port, username=username, password=password),
            normalized_path if normalized_scheme in {"ws", "wss"} else "",
            "",
            "",
        )
    )


def _build_netloc(host: str, port: int, username: str | None, password: str | None) -> str:
    credentials = ""
    if username:
        credentials = quote(username, safe="")
        if password:
            credentials = f"{credentials}:{quote(password, safe='')}"
        credentials = f"{credentials}@"
    return f"{credentials}{host}:{port}"


def _normalize_cdp_path(path: str) -> str:
    normalized_path = path.strip() or "/devtools/browser"
    if normalized_path.startswith("/"):
        return normalized_path
    return f"/{normalized_path}"


def _is_full_browser_ws_path(path: str) -> bool:
    return path.startswith("/devtools/browser/")


def _normalize_cdp_scheme(scheme: str, path: str) -> str:
    normalized_scheme = scheme.lower()
    if normalized_scheme in {"http", "https"}:
        return normalized_scheme
    if normalized_scheme in {"ws", "wss"}:
        if _is_full_browser_ws_path(path):
            return normalized_scheme
        return "http" if normalized_scheme == "ws" else "https"
    return "http"


def _open_browser_page(browser: Browser, source: str) -> PlaywrightPageSession:
    context = browser.contexts[0] if browser.contexts else browser.new_context(
        locale=DEFAULT_LOCALE,
        user_agent=DEFAULT_USER_AGENT,
    )
    page = context.new_page()
    return PlaywrightPageSession(page=page, source=source, _owned_context=None)
