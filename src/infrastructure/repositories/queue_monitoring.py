from core.monitoring.models import QueueJob, QueueStats
from infrastructure.queues.monitoring import (
    QueueJob as InfraQueueJob,
)
from infrastructure.queues.monitoring import (
    QueueStats as InfraQueueStats,
)
from infrastructure.queues.monitoring import count_queue_jobs as count_infra_queue_jobs
from infrastructure.queues.monitoring import get_queue_stats as get_infra_queue_stats
from infrastructure.queues.monitoring import list_queue_jobs as list_infra_queue_jobs


class QueueMonitoringRepository:
    def get_queue_stats(self) -> QueueStats:
        return _map_queue_stats(get_infra_queue_stats())

    def list_queue_jobs(self, limit: int = 50, offset: int = 0, status_filter: str | None = None) -> list[QueueJob]:
        return [
            _map_queue_job(queue_job)
            for queue_job in list_infra_queue_jobs(limit=limit, offset=offset, status_filter=status_filter)
        ]

    def count_queue_jobs(self, status_filter: str | None = None) -> int:
        return count_infra_queue_jobs(status_filter=status_filter)


def get_queue_monitoring_repository() -> QueueMonitoringRepository:
    global _queue_monitoring_repository
    if _queue_monitoring_repository is None:
        _queue_monitoring_repository = QueueMonitoringRepository()
    return _queue_monitoring_repository


def _map_queue_stats(stats: InfraQueueStats) -> QueueStats:
    return QueueStats(
        total=stats.total,
        pending=stats.pending,
        running=stats.running,
        done=stats.done,
        failed=stats.failed,
    )


def _map_queue_job(queue_job: InfraQueueJob) -> QueueJob:
    return QueueJob(
        id=queue_job.id,
        name=queue_job.name,
        status=queue_job.status,
        attempt=queue_job.attempt,
        max_retries=queue_job.max_retries,
        updated_at=queue_job.updated_at,
        created_at=queue_job.created_at,
        finished_at=queue_job.finished_at,
        last_error=queue_job.last_error,
    )


_queue_monitoring_repository: QueueMonitoringRepository | None = None
