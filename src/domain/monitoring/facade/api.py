from domain.monitoring.models import QueueJob, QueueStats
from domain.monitoring.services import QueueMonitoringManager

from .runtime import get_queue_monitoring_manager


def get_queue_stats() -> QueueStats:
    return _get_manager().get_queue_stats()


def list_queue_jobs(limit: int = 50) -> list[QueueJob]:
    return _get_manager().list_queue_jobs(limit=limit)


def _get_manager() -> QueueMonitoringManager:
    return get_queue_monitoring_manager()
