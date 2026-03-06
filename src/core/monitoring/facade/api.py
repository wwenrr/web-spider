from core.monitoring.models import QueueJob, QueueStats
from core.monitoring.services import QueueMonitoringManager

from .runtime import get_queue_monitoring_manager


def get_queue_stats() -> QueueStats:
    return _get_manager().get_queue_stats()


def list_queue_jobs(limit: int = 50, offset: int = 0, status_filter: str | None = None) -> list[QueueJob]:
    return _get_manager().list_queue_jobs(limit=limit, offset=offset, status_filter=status_filter)


def count_queue_jobs(status_filter: str | None = None) -> int:
    return _get_manager().count_queue_jobs(status_filter=status_filter)


def _get_manager() -> QueueMonitoringManager:
    return get_queue_monitoring_manager()
