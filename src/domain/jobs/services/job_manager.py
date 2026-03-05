from domain.jobs.constants import AUDIT_EVENT_JOB_CREATED
from domain.jobs.interfaces import IJobQueue, IJobRepository
from models.todo import Todo


class JobManager:
    def __init__(self, repository: IJobRepository, queue: IJobQueue | None = None) -> None:
        self._repository = repository
        self._queue = queue

    def list_jobs(self) -> list[Todo]:
        return self._repository.list_jobs()

    def create_job(self, title: str) -> None:
        self._repository.create_job(title)

    def create_job_with_audit(self, title: str) -> None:
        self.create_job(title)
        if self._queue is not None:
            self._queue.enqueue(AUDIT_EVENT_JOB_CREATED, title)

    def get_job(self, job_id: int) -> Todo | None:
        return self._repository.get_job(job_id)

    def update_job(self, job_id: int, title: str) -> bool:
        return self._repository.update_job(job_id, title)

    def toggle_job(self, job_id: int) -> None:
        self._repository.toggle_job(job_id)

    def delete_job(self, job_id: int) -> bool:
        return self._repository.delete_job(job_id)
