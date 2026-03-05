from .job_manager import JobManager

_job_manager: JobManager | None = None


def configure_job_manager(job_manager: JobManager) -> None:
    global _job_manager
    _job_manager = job_manager


def get_job_manager() -> JobManager:
    if _job_manager is None:
        raise RuntimeError("JobManager is not configured")
    return _job_manager
