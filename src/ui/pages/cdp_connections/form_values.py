from dataclasses import dataclass
from typing import Final

from nicegui import ui

from models.cdp_connection import CdpConnection

PORT_PARSE_ERROR_MESSAGE: Final[str] = "Port phải là số nguyên hợp lệ"


@dataclass(frozen=True)
class ConnectionFormValues:
    name: str
    host: str
    port: int
    browser: str
    ws_path: str
    username: str | None
    password: str | None
    is_active: bool
    notes: str | None


async def read_form_values(form_key: str) -> ConnectionFormValues:
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
                host: read('{form_key}-host'),
                port: read('{form_key}-port'),
                browser: read('{form_key}-browser'),
                wsPath: read('{form_key}-ws-path'),
                username: read('{form_key}-username'),
                password: read('{form_key}-password'),
                notes: read('{form_key}-notes'),
                isActive: readChecked('{form_key}-is-active'),
            }};
        }})()"""
    )

    payload = raw if isinstance(raw, dict) else {}
    return ConnectionFormValues(
        name=str(payload.get("name", "")).strip(),
        host=str(payload.get("host", "")).strip(),
        port=_parse_port(payload.get("port")),
        browser=str(payload.get("browser", "")).strip(),
        ws_path=str(payload.get("wsPath", "")).strip(),
        username=_normalize_optional_text(payload.get("username")),
        password=_normalize_optional_text(payload.get("password")),
        is_active=bool(payload.get("isActive", False)),
        notes=_normalize_optional_text(payload.get("notes")),
    )


def defaults_from_connection(connection: CdpConnection | None) -> ConnectionFormValues:
    if connection is None:
        return ConnectionFormValues(
            name="",
            host="",
            port=9222,
            browser="chrome",
            ws_path="/devtools/browser",
            username=None,
            password=None,
            is_active=True,
            notes=None,
        )

    return ConnectionFormValues(
        name=connection.name,
        host=connection.host,
        port=connection.port,
        browser=connection.browser,
        ws_path=connection.ws_path,
        username=connection.username,
        password=connection.password,
        is_active=connection.is_active,
        notes=connection.notes,
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
