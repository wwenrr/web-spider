from models.todo import Todo

from .job_manager import JobManager
from .scheduler_service import SchedulerService

_job_manager: JobManager | None = None


def configure_job_manager(job_manager: JobManager) -> None:
    global _job_manager
    _job_manager = job_manager


def get_job_manager() -> JobManager:
    if _job_manager is None:
        raise RuntimeError("JobManager is not configured")
    return _job_manager


def create_job(title: str) -> None:
    get_job_manager().create_job(title)


def create_job_with_audit(title: str) -> None:
    get_job_manager().create_job_with_audit(title)


def delete_job(job_id: int) -> bool:
    return get_job_manager().delete_job(job_id)


def get_job(job_id: int) -> Todo | None:
    return get_job_manager().get_job(job_id)


def list_jobs() -> list[Todo]:
    return get_job_manager().list_jobs()


def toggle_job(job_id: int) -> None:
    get_job_manager().toggle_job(job_id)


def update_job(job_id: int, title: str) -> bool:
    return get_job_manager().update_job(job_id, title)

__all__ = [
    "JobManager",
    "SchedulerService",
    "configure_job_manager",
    "create_job",
    "create_job_with_audit",
    "delete_job",
    "get_job",
    "get_job_manager",
    "list_jobs",
    "toggle_job",
    "update_job",
]
