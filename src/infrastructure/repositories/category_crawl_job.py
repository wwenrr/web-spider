from typing import Final, cast
from urllib.parse import urlsplit, urlunsplit

from peewee import IntegrityError

from infrastructure.database import database
from infrastructure.models.category_crawl_job import CategoryCrawlJob, CategoryCrawlStatus, utc_now

ACTIVE_CATEGORY_CRAWL_MESSAGE: Final[str] = "Category crawl is already pending or processing."
EMPTY_CATEGORY_NAME_MESSAGE: Final[str] = "Category name cannot be empty."
EMPTY_CATEGORY_URL_MESSAGE: Final[str] = "Category URL cannot be empty."
INVALID_CATEGORY_URL_MESSAGE: Final[str] = "Category URL must start with http:// or https://."


class CategoryCrawlJobRepository:
    def list_jobs(self, limit: int = 50) -> list[CategoryCrawlJob]:
        with database:
            return list(CategoryCrawlJob.select().order_by(CategoryCrawlJob.created_at.desc()).limit(limit))

    def get_job(self, job_id: int) -> CategoryCrawlJob | None:
        with database:
            return CategoryCrawlJob.get_or_none(CategoryCrawlJob.id == job_id)

    def create_pending_job(self, site_key: str, category_name: str, category_url: str) -> CategoryCrawlJob:
        payload = _build_pending_payload(site_key, category_name, category_url)
        if self.has_active_job(payload["normalized_category_url"]):
            raise ValueError(ACTIVE_CATEGORY_CRAWL_MESSAGE)

        with database:
            try:
                return cast(CategoryCrawlJob, CategoryCrawlJob.create(**payload))
            except IntegrityError as exc:
                raise ValueError(ACTIVE_CATEGORY_CRAWL_MESSAGE) from exc

    def mark_processing(self, job_id: int) -> bool:
        with database:
            updated_rows = cast(
                int,
                CategoryCrawlJob.update(
                    crawl_status=CategoryCrawlStatus.PROCESSING.value,
                    error_message=None,
                    updated_at=utc_now(),
                )
                .where(CategoryCrawlJob.id == job_id)
                .execute(),
            )
        return updated_rows > 0

    def mark_done(
        self,
        job_id: int,
        total_products: int,
        products_per_page: int,
        total_pages: int,
        enqueued_products_count: int,
    ) -> bool:
        with database:
            updated_rows = cast(
                int,
                CategoryCrawlJob.update(
                    crawl_status=CategoryCrawlStatus.DONE.value,
                    total_products=total_products,
                    products_per_page=products_per_page,
                    total_pages=total_pages,
                    enqueued_products_count=enqueued_products_count,
                    crawl_at=utc_now(),
                    error_message=None,
                    updated_at=utc_now(),
                )
                .where(CategoryCrawlJob.id == job_id)
                .execute(),
            )
        return updated_rows > 0

    def mark_failed(self, job_id: int, error_message: str) -> bool:
        with database:
            updated_rows = cast(
                int,
                CategoryCrawlJob.update(
                    crawl_status=CategoryCrawlStatus.FAILED.value,
                    error_message=error_message.strip() or "Category crawl failed.",
                    updated_at=utc_now(),
                )
                .where(CategoryCrawlJob.id == job_id)
                .execute(),
            )
        return updated_rows > 0

    def has_active_job(self, normalized_category_url: str) -> bool:
        with database:
            existing = (
                CategoryCrawlJob.select(CategoryCrawlJob.id)
                .where(
                    (CategoryCrawlJob.normalized_category_url == normalized_category_url)
                    & (
                        (CategoryCrawlJob.crawl_status == CategoryCrawlStatus.PENDING.value)
                        | (CategoryCrawlJob.crawl_status == CategoryCrawlStatus.PROCESSING.value)
                    )
                )
                .first()
            )
        return existing is not None


def get_category_crawl_job_repository() -> CategoryCrawlJobRepository:
    global _category_crawl_job_repository
    if _category_crawl_job_repository is None:
        _category_crawl_job_repository = CategoryCrawlJobRepository()
    return _category_crawl_job_repository


def _build_pending_payload(site_key: str, category_name: str, category_url: str) -> dict[str, object]:
    normalized_site_key = site_key.strip() or "1999"
    normalized_category_name = category_name.strip()
    if normalized_category_name == "":
        raise ValueError(EMPTY_CATEGORY_NAME_MESSAGE)

    normalized_category_url = _normalize_category_url(category_url)
    return {
        "site_key": normalized_site_key,
        "category_name": normalized_category_name,
        "category_url": normalized_category_url,
        "normalized_category_url": normalized_category_url,
        "crawl_status": CategoryCrawlStatus.PENDING.value,
        "total_products": None,
        "products_per_page": None,
        "total_pages": None,
        "enqueued_products_count": None,
        "crawl_at": None,
        "error_message": None,
        "updated_at": utc_now(),
    }


def _normalize_category_url(raw_category_url: str) -> str:
    normalized_category_url = raw_category_url.strip()
    if normalized_category_url == "":
        raise ValueError(EMPTY_CATEGORY_URL_MESSAGE)
    if not (normalized_category_url.startswith("http://") or normalized_category_url.startswith("https://")):
        raise ValueError(INVALID_CATEGORY_URL_MESSAGE)

    parts = urlsplit(normalized_category_url)
    normalized_path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme, parts.netloc, normalized_path, parts.query, ""))


_category_crawl_job_repository: CategoryCrawlJobRepository | None = None
