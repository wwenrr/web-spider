from core.monitoring.interfaces import IQueueMonitoringRepository
from core.monitoring.models import QueueJob, QueueStats


class QueueMonitoringManager:
    def __init__(self, repository: IQueueMonitoringRepository) -> None:
        self._repository = repository

    def get_queue_stats(self) -> QueueStats:
        return self._repository.get_queue_stats()

    def list_queue_jobs(self, limit: int = 50) -> list[QueueJob]:
        return self._repository.list_queue_jobs(limit=limit)
