from models.todo import Todo

from .job_manager import JobManager
from .runtime import get_job_manager


def create_job(title: str) -> None:
    _get_manager().create_job(title)


def delete_job(job_id: int) -> bool:
    return _get_manager().delete_job(job_id)


def list_jobs() -> list[Todo]:
    return _get_manager().list_jobs()


def toggle_job(job_id: int) -> None:
    _get_manager().toggle_job(job_id)


def update_job(job_id: int, title: str) -> bool:
    return _get_manager().update_job(job_id, title)


def _get_manager() -> JobManager:
    return get_job_manager()
