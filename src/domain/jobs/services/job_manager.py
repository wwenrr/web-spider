from domain.jobs.interfaces import IJobRepository
from models.todo import Todo


class JobManager:
    def __init__(self, repository: IJobRepository) -> None:
        self._repository = repository

    def list_jobs(self) -> list[Todo]:
        return self._repository.list_jobs()

    def create_job(self, title: str) -> None:
        self._repository.create_job(title)

    def update_job(self, job_id: int, title: str) -> bool:
        return self._repository.update_job(job_id, title)

    def toggle_job(self, job_id: int) -> None:
        self._repository.toggle_job(job_id)

    def delete_job(self, job_id: int) -> bool:
        return self._repository.delete_job(job_id)
