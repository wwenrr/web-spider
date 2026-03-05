from core.cdp_connections.services import CdpConnectionManager

_cdp_connection_manager: CdpConnectionManager | None = None


def configure_cdp_connection_manager(cdp_connection_manager: CdpConnectionManager) -> None:
    global _cdp_connection_manager
    _cdp_connection_manager = cdp_connection_manager


def get_cdp_connection_manager() -> CdpConnectionManager:
    if _cdp_connection_manager is None:
        raise RuntimeError("CdpConnectionManager is not configured")
    return _cdp_connection_manager
