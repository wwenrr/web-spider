from dataclasses import dataclass
from typing import Final

from nicegui import ui

from infrastructure.models.managed_browser import ManagedBrowser

PORT_PARSE_ERROR_MESSAGE: Final[str] = "Port must be a valid integer."


@dataclass(frozen=True)
class ManagedBrowserFormValues:
    name: str
    browser_type: str
    host: str
    port: int
    executable_path: str | None
    user_data_dir: str
    headless: bool
    launch_args: str | None
    is_active: bool
    notes: str | None


async def read_form_values(form_key: str) -> ManagedBrowserFormValues:
    raw = await ui.run_javascript(
        f"""(() => {{
            const read = (id) => {{
                const element = document.getElementById(id);
                return element ? element.value : '';
            }};
            const readChecked = (id) => {{
                const element = document.getElementById(id);
                return Boolean(element && element.checked);
            }};
            return {{
                name: read('{form_key}-name'),
                browserType: read('{form_key}-browser-type'),
                host: read('{form_key}-host'),
                port: read('{form_key}-port'),
                executablePath: read('{form_key}-executable-path'),
                userDataDir: read('{form_key}-user-data-dir'),
                launchArgs: read('{form_key}-launch-args'),
                notes: read('{form_key}-notes'),
                headless: readChecked('{form_key}-headless'),
                isActive: readChecked('{form_key}-is-active'),
            }};
        }})()"""
    )
    payload = raw if isinstance(raw, dict) else {}
    return ManagedBrowserFormValues(
        name=str(payload.get("name", "")).strip(),
        browser_type=str(payload.get("browserType", "")).strip(),
        host=str(payload.get("host", "")).strip(),
        port=_parse_port(payload.get("port")),
        executable_path=_normalize_optional_text(payload.get("executablePath")),
        user_data_dir=str(payload.get("userDataDir", "")).strip(),
        headless=bool(payload.get("headless", False)),
        launch_args=_normalize_optional_text(payload.get("launchArgs")),
        is_active=bool(payload.get("isActive", False)),
        notes=_normalize_optional_text(payload.get("notes")),
    )


def defaults_from_browser(browser: ManagedBrowser | None) -> ManagedBrowserFormValues:
    if browser is None:
        return ManagedBrowserFormValues(
            name="",
            browser_type="chrome",
            host="127.0.0.1",
            port=9333,
            executable_path=None,
            user_data_dir="/tmp/web-spider-managed-browser",
            headless=False,
            launch_args=None,
            is_active=True,
            notes=None,
        )

    return ManagedBrowserFormValues(
        name=browser.name,
        browser_type=browser.browser_type,
        host=browser.host,
        port=browser.port,
        executable_path=browser.executable_path,
        user_data_dir=browser.user_data_dir,
        headless=browser.headless,
        launch_args=browser.launch_args,
        is_active=browser.is_active,
        notes=browser.notes,
    )


def _parse_port(raw_port: object) -> int:
    as_text = str(raw_port or "").strip()
    if as_text == "":
        raise ValueError(PORT_PARSE_ERROR_MESSAGE)
    try:
        return int(as_text)
    except ValueError as exc:
        raise ValueError(PORT_PARSE_ERROR_MESSAGE) from exc


def _normalize_optional_text(value: object) -> str | None:
    normalized = str(value or "").strip()
    if normalized == "":
        return None
    return normalized
