import os
import shlex
import shutil
import signal
import subprocess
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from infrastructure.models.managed_browser import ManagedBrowser, ManagedBrowserStatus
from infrastructure.repositories.managed_browser import get_managed_browser_repository

BROWSER_START_TIMEOUT_SECONDS = 15.0
BROWSER_START_POLL_INTERVAL_SECONDS = 0.5
DEFAULT_BROWSER_URL = "about:blank"


class ManagedBrowserRuntime:
    def __init__(self) -> None:
        self._repository = get_managed_browser_repository()

    def list_browsers(self) -> list[ManagedBrowser]:
        browsers = self._repository.list_browsers()
        return [self.refresh_browser_state(browser.id) or browser for browser in browsers]

    def ensure_active_browser(self, *, headless: bool) -> ManagedBrowser:
        browser = self._repository.get_active_browser()
        if browser is None:
            browser = self._repository.ensure_default_active_browser(headless=headless)

        refreshed_browser = self.refresh_browser_state(browser.id)
        if refreshed_browser is not None and _is_browser_endpoint_ready(refreshed_browser):
            self._repository.touch_seen(refreshed_browser.id)
            latest = self._repository.get_browser(refreshed_browser.id)
            if latest is not None:
                return latest
            return refreshed_browser

        return self.start_browser(browser.id)

    def start_browser(self, browser_id: int) -> ManagedBrowser:
        browser = self._require_browser(browser_id)
        refreshed_browser = self.refresh_browser_state(browser_id)
        if refreshed_browser is not None and _is_browser_endpoint_ready(refreshed_browser):
            self._repository.touch_seen(browser_id)
            latest = self._repository.get_browser(browser_id)
            if latest is not None:
                return latest
            return refreshed_browser

        if not self._repository.claim_starting(browser_id):
            waited_browser = self._wait_until_ready(browser_id)
            if waited_browser is not None:
                return waited_browser
            raise ValueError("Managed browser is already starting.")

        browser_to_start = self._require_browser(browser_id)
        try:
            process = _launch_browser_process(browser_to_start)
            started_browser = self._wait_until_ready(browser_id, fallback_pid=process.pid)
            if started_browser is None:
                raise RuntimeError("Timed out while waiting for the browser CDP endpoint.")
            return started_browser
        except Exception as exc:
            self._repository.mark_failed(browser_id, str(exc))
            raise

    def stop_browser(self, browser_id: int) -> ManagedBrowser:
        browser = self._require_browser(browser_id)
        if browser.pid is not None and _is_process_alive(browser.pid):
            os.kill(browser.pid, signal.SIGTERM)
            for _ in range(10):
                if not _is_process_alive(browser.pid):
                    break
                time.sleep(0.2)
            if _is_process_alive(browser.pid):
                os.kill(browser.pid, signal.SIGKILL)

        self._repository.mark_stopped(browser_id)
        refreshed = self._repository.get_browser(browser_id)
        if refreshed is None:
            raise ValueError("Managed browser no longer exists.")
        return refreshed

    def refresh_browser_state(self, browser_id: int) -> ManagedBrowser | None:
        browser = self._repository.get_browser(browser_id)
        if browser is None:
            return None

        if _is_browser_endpoint_ready(browser):
            if browser.status == ManagedBrowserStatus.RUNNING.value:
                self._repository.touch_seen(browser.id)
            else:
                self._repository.mark_running(browser.id, browser.pid)
            refreshed = self._repository.get_browser(browser.id)
            return refreshed if refreshed is not None else browser

        if browser.status in {ManagedBrowserStatus.RUNNING.value, ManagedBrowserStatus.STARTING.value}:
            if browser.pid is not None and _is_process_alive(browser.pid):
                self._repository.mark_failed(browser.id, "Browser process is alive but the CDP endpoint is unreachable.")
            else:
                self._repository.mark_stopped(browser.id)

        return self._repository.get_browser(browser.id)

    def endpoint_for(self, browser: ManagedBrowser) -> str:
        return _build_browser_endpoint(browser)

    def _require_browser(self, browser_id: int) -> ManagedBrowser:
        browser = self._repository.get_browser(browser_id)
        if browser is None:
            raise ValueError(f"Managed browser not found: {browser_id}")
        return browser

    def _wait_until_ready(self, browser_id: int, fallback_pid: int | None = None) -> ManagedBrowser | None:
        deadline = time.monotonic() + BROWSER_START_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            browser = self._repository.get_browser(browser_id)
            if browser is None:
                return None
            if _is_browser_endpoint_ready(browser):
                self._repository.mark_running(browser.id, browser.pid or fallback_pid)
                refreshed = self._repository.get_browser(browser.id)
                if refreshed is not None:
                    return refreshed
                return browser
            time.sleep(BROWSER_START_POLL_INTERVAL_SECONDS)
        return None


_managed_browser_runtime: ManagedBrowserRuntime | None = None


def get_managed_browser_runtime() -> ManagedBrowserRuntime:
    global _managed_browser_runtime
    if _managed_browser_runtime is None:
        _managed_browser_runtime = ManagedBrowserRuntime()
    return _managed_browser_runtime


def _launch_browser_process(browser: ManagedBrowser) -> subprocess.Popen[bytes]:
    executable_path = _resolve_executable_path(browser)
    profile_dir = Path(browser.user_data_dir).expanduser()
    profile_dir.mkdir(parents=True, exist_ok=True)
    command = [
        executable_path,
        f"--remote-debugging-address={browser.host}",
        f"--remote-debugging-port={browser.port}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--disable-sync",
        "--disable-dev-shm-usage",
    ]
    if browser.headless:
        command.append("--headless=new")
    if browser.launch_args:
        command.extend(shlex.split(browser.launch_args))
    command.append(DEFAULT_BROWSER_URL)
    return subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def _resolve_executable_path(browser: ManagedBrowser) -> str:
    if browser.executable_path:
        executable_path = Path(browser.executable_path).expanduser()
        if executable_path.exists():
            return str(executable_path)
        raise ValueError(f"Browser executable not found: {browser.executable_path}")

    candidates = _browser_candidates(browser.browser_type)
    for candidate in candidates:
        resolved = shutil.which(candidate)
        if resolved is not None:
            return resolved
    raise ValueError(f"No executable found for browser type: {browser.browser_type}")


def _browser_candidates(browser_type: str) -> tuple[str, ...]:
    normalized = browser_type.strip().lower()
    if normalized in {"chrome", "google-chrome"}:
        return ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
    if normalized in {"chromium", "chromium-browser"}:
        return ("chromium", "chromium-browser", "google-chrome")
    return (normalized, "google-chrome", "chromium", "chromium-browser")


def _is_browser_endpoint_ready(browser: ManagedBrowser) -> bool:
    try:
        with urlopen(f"http://{browser.host}:{browser.port}/json/version", timeout=1.5) as response:
            return response.status == 200
    except (OSError, URLError):
        return False


def _is_process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def _build_browser_endpoint(browser: ManagedBrowser) -> str:
    return f"http://{browser.host}:{browser.port}"
