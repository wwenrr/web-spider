from typing import Protocol

from core.monitoring.models import QueueJob, QueueStats


class IQueueMonitoringRepository(Protocol):
    def get_queue_stats(self) -> QueueStats: ...
    def list_queue_jobs(self, limit: int = 50) -> list[QueueJob]: ...
