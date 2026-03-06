from core.category_crawls.services import CategoryCrawlManager

_category_crawl_manager: CategoryCrawlManager | None = None


def configure_category_crawl_manager(category_crawl_manager: CategoryCrawlManager) -> None:
    global _category_crawl_manager
    _category_crawl_manager = category_crawl_manager


def get_category_crawl_manager() -> CategoryCrawlManager:
    if _category_crawl_manager is None:
        raise RuntimeError("CategoryCrawlManager is not configured")
    return _category_crawl_manager
