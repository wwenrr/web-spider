from core.category_crawls.constants import CRAWL_EVENT_CATEGORY_JOB
from core.category_crawls.interfaces import ICategoryCrawlJobRepository, ICategoryCrawlQueue
from infrastructure.models.category_crawl_job import CategoryCrawlJob


class CategoryCrawlManager:
    def __init__(
        self,
        repository: ICategoryCrawlJobRepository,
        task_queue: ICategoryCrawlQueue | None = None,
    ) -> None:
        self._repository = repository
        self._task_queue = task_queue

    def list_jobs(self, limit: int = 50) -> list[CategoryCrawlJob]:
        return self._repository.list_jobs(limit=limit)

    def enqueue_category_crawl(self, category_name: str, category_url: str, site_key: str = "1999") -> CategoryCrawlJob:
        job = self._repository.create_pending_job(site_key=site_key, category_name=category_name, category_url=category_url)
        if self._task_queue is not None:
            self._task_queue.enqueue(CRAWL_EVENT_CATEGORY_JOB, job.id)
        return job
