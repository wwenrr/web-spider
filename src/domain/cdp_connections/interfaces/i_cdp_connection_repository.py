from typing import Protocol

from models.cdp_connection import CdpConnection


class ICdpConnectionRepository(Protocol):
    def list_connections(self) -> list[CdpConnection]: ...

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
    ) -> None: ...

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
    ) -> bool: ...

    def delete_connection(self, connection_id: int) -> bool: ...
