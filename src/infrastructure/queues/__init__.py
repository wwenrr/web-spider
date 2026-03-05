from .monitoring import QueueJob, QueueStats, get_queue_stats, list_queue_jobs
from .pybgworker_queue import PybgworkerQueue
from .task_registry import resolve_task

_job_queue: PybgworkerQueue | None = None


def get_default_job_queue() -> PybgworkerQueue:
    global _job_queue
    if _job_queue is None:
        _job_queue = PybgworkerQueue()
    return _job_queue


__all__ = [
    "PybgworkerQueue",
    "QueueJob",
    "QueueStats",
    "get_default_job_queue",
    "get_queue_stats",
    "list_queue_jobs",
    "resolve_task",
]
