from typing import Final, cast

from infrastructure.database import database
from infrastructure.models.cdp_connection import CdpConnection, utc_now

EMPTY_NAME_MESSAGE: Final[str] = "Tên connection không được để trống"
EMPTY_HOST_MESSAGE: Final[str] = "Host không được để trống"
INVALID_PORT_MESSAGE: Final[str] = "Port phải nằm trong khoảng 1-65535"


class CdpConnectionRepository:
    def list_connections(self) -> list[CdpConnection]:
        with database:
            return list(CdpConnection.select().order_by(CdpConnection.created_at.desc()))

    def create_connection(
        self,
        name: str,
        host: str,
        port: int,
        browser: str,
        ws_path: str,
        username: str | None,
        password: str | None,
        is_active: bool,
        notes: str | None,
    ) -> None:
        payload = _build_validated_payload(name, host, port, browser, ws_path, username, password, is_active, notes)
        with database:
            CdpConnection.create(**payload)

    def update_connection(
        self,
        connection_id: int,
        name: str,
        host: str,
        port: int,
        browser: str,
        ws_path: str,
        username: str | None,
        password: str | None,
        is_active: bool,
        notes: str | None,
    ) -> bool:
        payload = _build_validated_payload(name, host, port, browser, ws_path, username, password, is_active, notes)
        with database:
            updated_rows = cast(
                int,
                CdpConnection.update(**payload, updated_at=utc_now())
                .where(CdpConnection.id == connection_id)
                .execute(),
            )
        return updated_rows > 0

    def delete_connection(self, connection_id: int) -> bool:
        with database:
            deleted_rows = cast(
                int,
                CdpConnection.delete().where(CdpConnection.id == connection_id).execute(),
            )
        return deleted_rows > 0


def _build_validated_payload(
    name: str,
    host: str,
    port: int,
    browser: str,
    ws_path: str,
    username: str | None,
    password: str | None,
    is_active: bool,
    notes: str | None,
) -> dict[str, object]:
    normalized_name = name.strip()
    if normalized_name == "":
        raise ValueError(EMPTY_NAME_MESSAGE)

    normalized_host = host.strip()
    if normalized_host == "":
        raise ValueError(EMPTY_HOST_MESSAGE)

    if port < 1 or port > 65535:
        raise ValueError(INVALID_PORT_MESSAGE)

    normalized_browser = browser.strip() or "chrome"
    normalized_ws_path = ws_path.strip() or "/devtools/browser"

    return {
        "name": normalized_name,
        "host": normalized_host,
        "port": port,
        "browser": normalized_browser,
        "ws_path": normalized_ws_path,
        "username": _optional_text(username),
        "password": _optional_text(password),
        "is_active": is_active,
        "notes": _optional_text(notes),
    }


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    if normalized == "":
        return None

    return normalized


_cdp_connection_repository: CdpConnectionRepository | None = None


def get_cdp_connection_repository() -> CdpConnectionRepository:
    global _cdp_connection_repository
    if _cdp_connection_repository is None:
        _cdp_connection_repository = CdpConnectionRepository()
    return _cdp_connection_repository
