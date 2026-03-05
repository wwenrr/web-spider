from domain.monitoring.services import QueueMonitoringManager

_queue_monitoring_manager: QueueMonitoringManager | None = None


def configure_queue_monitoring_manager(queue_monitoring_manager: QueueMonitoringManager) -> None:
    global _queue_monitoring_manager
    _queue_monitoring_manager = queue_monitoring_manager


def get_queue_monitoring_manager() -> QueueMonitoringManager:
    if _queue_monitoring_manager is None:
        raise RuntimeError("QueueMonitoringManager is not configured")
    return _queue_monitoring_manager
