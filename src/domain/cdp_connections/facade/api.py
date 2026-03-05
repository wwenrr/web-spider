from domain.cdp_connections.services import CdpConnectionManager
from models.cdp_connection import CdpConnection

from .runtime import get_cdp_connection_manager


def list_cdp_connections() -> list[CdpConnection]:
    return _get_manager().list_connections()


def create_cdp_connection(
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
    _get_manager().create_connection(name, host, port, browser, ws_path, username, password, is_active, notes)


def update_cdp_connection(
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
    return _get_manager().update_connection(
        connection_id,
        name,
        host,
        port,
        browser,
        ws_path,
        username,
        password,
        is_active,
        notes,
    )


def delete_cdp_connection(connection_id: int) -> bool:
    return _get_manager().delete_connection(connection_id)


def _get_manager() -> CdpConnectionManager:
    return get_cdp_connection_manager()
