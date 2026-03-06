from core.category_crawls.services import CategoryCrawlManager
from infrastructure.models.category_crawl_job import CategoryCrawlJob

from .runtime import get_category_crawl_manager


def list_category_crawl_jobs(limit: int = 50) -> list[CategoryCrawlJob]:
    return _get_manager().list_jobs(limit=limit)


def enqueue_category_crawl(category_name: str, category_url: str, site_key: str = "1999") -> CategoryCrawlJob:
    return _get_manager().enqueue_category_crawl(
        category_name=category_name,
        category_url=category_url,
        site_key=site_key,
    )


def _get_manager() -> CategoryCrawlManager:
    return get_category_crawl_manager()
