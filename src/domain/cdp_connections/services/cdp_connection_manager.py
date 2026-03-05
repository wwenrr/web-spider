from domain.cdp_connections.interfaces import ICdpConnectionRepository
from models.cdp_connection import CdpConnection


class CdpConnectionManager:
    def __init__(self, repository: ICdpConnectionRepository) -> None:
        self._repository = repository

    def list_connections(self) -> list[CdpConnection]:
        return self._repository.list_connections()

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
        self._repository.create_connection(name, host, port, browser, ws_path, username, password, is_active, notes)

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
        return self._repository.update_connection(
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

    def delete_connection(self, connection_id: int) -> bool:
        return self._repository.delete_connection(connection_id)
