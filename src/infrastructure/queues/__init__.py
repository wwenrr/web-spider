from .pybgworker_queue import PybgworkerQueue
from .task_registry import resolve_task

_job_queue: PybgworkerQueue | None = None


def get_default_job_queue() -> PybgworkerQueue:
    global _job_queue
    if _job_queue is None:
        _job_queue = PybgworkerQueue()
    return _job_queue


__all__ = ["PybgworkerQueue", "get_default_job_queue", "resolve_task"]
