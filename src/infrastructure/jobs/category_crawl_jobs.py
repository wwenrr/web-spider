from pathlib import Path
from typing import Final
import os

from pybgworker import utils as bg_utils
from pybgworker.task import task

from infrastructure.adapters.spiders.hobby_search_category_spider import HobbySearchCategorySpider
from infrastructure.constants.db import DB_DIR_PATH
from infrastructure.constants.queue import TASK_CRAWL_CATEGORY_JOB, TASK_CRAWL_PRODUCT_URL
from infrastructure.helpers.settings import get_bgworker_max_retries
from infrastructure.repositories.category_crawl_job import get_category_crawl_job_repository
from infrastructure.repositories.product import get_product_repository
from infrastructure.queues import get_default_job_queue

DB_DIR: Final[Path] = DB_DIR_PATH
DB_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("PYBGWORKER_DB", str(DB_DIR / "pybgworker.db"))
bg_utils.DB_PATH = os.environ["PYBGWORKER_DB"]


@task(name=TASK_CRAWL_CATEGORY_JOB, retries=get_bgworker_max_retries())
def crawl_category_job(category_crawl_job_id: int) -> None:
    category_repository = get_category_crawl_job_repository()
    category_job = category_repository.get_job(category_crawl_job_id)
    if category_job is None:
        raise ValueError(f"Category crawl job not found: {category_crawl_job_id}")

    category_repository.mark_processing(category_crawl_job_id)
    try:
        parsed_category = HobbySearchCategorySpider().crawl(category_job.category_url)
        enqueued_products_count = _enqueue_product_urls(parsed_category.product_urls)
        updated = category_repository.mark_done(
            job_id=category_crawl_job_id,
            total_products=parsed_category.total_products,
            products_per_page=parsed_category.products_per_page,
            total_pages=parsed_category.total_pages,
            enqueued_products_count=enqueued_products_count,
        )
        if not updated:
            raise RuntimeError(f"Failed to update category crawl job: {category_crawl_job_id}")
    except Exception as exc:
        category_repository.mark_failed(category_crawl_job_id, str(exc))
        raise


def _enqueue_product_urls(product_urls: list[str]) -> int:
    product_repository = get_product_repository()
    job_queue = get_default_job_queue()
    enqueued_products_count = 0
    for product_url in product_urls:
        product = product_repository.create_pending_product_if_missing(product_url)
        if product is None:
            continue
        job_queue.enqueue(TASK_CRAWL_PRODUCT_URL, product.id)
        enqueued_products_count += 1
    return enqueued_products_count
