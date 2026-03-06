from dataclasses import dataclass
from threading import Lock
from urllib.parse import quote, urlsplit, urlunsplit

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

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
        self._cdp_connection_id: int | None = None
        self._local_browser: Browser | None = None

    def open_page(self, *, headless: bool) -> PlaywrightPageSession:
        with self._lock:
            cdp_session = self._try_open_cdp_page()
            if cdp_session is not None:
                return cdp_session
            return self._open_local_page(headless=headless)

    def _try_open_cdp_page(self) -> PlaywrightPageSession | None:
        active_connection = _get_active_cdp_connection()
        if active_connection is None:
            self._disconnect_cdp_browser()
            return None

        browser = self._resolve_cdp_browser(active_connection)
        if browser is None:
            return None

        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        return PlaywrightPageSession(page=page, source="cdp", _owned_context=None)

    def _open_local_page(self, *, headless: bool) -> PlaywrightPageSession:
        playwright = self._get_playwright()
        if self._local_browser is None or not self._local_browser.is_connected():
            self._local_browser = playwright.chromium.launch(headless=headless)

        context = self._local_browser.new_context(
            locale=DEFAULT_LOCALE,
            user_agent=DEFAULT_USER_AGENT,
        )
        page = context.new_page()
        return PlaywrightPageSession(page=page, source="local", _owned_context=context)

    def _resolve_cdp_browser(self, connection: CdpConnection) -> Browser | None:
        if (
            self._cdp_browser is not None
            and self._cdp_browser.is_connected()
            and self._cdp_connection_id == connection.id
        ):
            return self._cdp_browser

        self._disconnect_cdp_browser()
        try:
            self._cdp_browser = self._get_playwright().chromium.connect_over_cdp(
                endpoint_url=_build_cdp_endpoint(connection),
            )
        except Exception:
            self._cdp_browser = None
            self._cdp_connection_id = None
            return None

        self._cdp_connection_id = connection.id
        return self._cdp_browser

    def _get_playwright(self) -> Playwright:
        if self._playwright is None:
            self._playwright = sync_playwright().start()
        return self._playwright

    def _disconnect_cdp_browser(self) -> None:
        if self._cdp_browser is None:
            self._cdp_connection_id = None
            return

        try:
            self._cdp_browser.close()
        except Exception:
            pass
        finally:
            self._cdp_browser = None
            self._cdp_connection_id = None


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


_shared_playwright_runtime: SharedPlaywrightRuntime | None = None
