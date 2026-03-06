from pathlib import Path
from typing import Final
import os
import time

from pybgworker import utils as bg_utils
from pybgworker.task import task

from infrastructure.adapters.spiders.hobby_search_product_spider import HobbySearchProductSpider
from infrastructure.constants.db import DB_DIR_PATH
from infrastructure.constants.queue import TASK_CRAWL_PRODUCT_URL
from infrastructure.repositories.product import get_product_repository

DB_DIR: Final[Path] = DB_DIR_PATH
DB_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("PYBGWORKER_DB", str(DB_DIR / "pybgworker.db"))
bg_utils.DB_PATH = os.environ["PYBGWORKER_DB"]


@task(name=TASK_CRAWL_PRODUCT_URL)
def crawl_product_url(product_id: int) -> None:
    repository = get_product_repository()
    product = repository.get_product(product_id)
    if product is None:
        raise ValueError(f"Product not found: {product_id}")

    repository.mark_product_crawl_processing(product_id)
    try:
        time.sleep(10)
        parsed_product = HobbySearchProductSpider().crawl(product.remote_url)
        updated = repository.update_product_crawl_result(
            product_id=product_id,
            thumbnail=parsed_product.thumbnail,
            name=parsed_product.name,
            category=parsed_product.category,
            price=parsed_product.price,
            images_url=parsed_product.images_url,
            barcode=parsed_product.barcode,
            code=parsed_product.code,
            remote_id=parsed_product.remote_id,
            remote_url=parsed_product.remote_url,
            description=parsed_product.description,
        )
        if not updated:
            raise RuntimeError(f"Failed to update crawled product: {product_id}")
    except Exception:
        repository.mark_product_crawl_failed(product_id)
        raise
