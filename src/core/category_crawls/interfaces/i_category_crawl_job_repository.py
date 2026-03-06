from typing import Protocol

from infrastructure.models.category_crawl_job import CategoryCrawlJob


class ICategoryCrawlJobRepository(Protocol):
    def list_jobs(self, limit: int = 50) -> list[CategoryCrawlJob]: ...

    def create_pending_job(self, site_key: str, category_name: str, category_url: str) -> CategoryCrawlJob: ...
