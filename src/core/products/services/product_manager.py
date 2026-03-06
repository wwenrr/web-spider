from core.products.constants import CRAWL_EVENT_PRODUCT_URL
from core.products.interfaces import IProductQueue, IProductRepository
from infrastructure.models.product import Product


class ProductManager:
    def __init__(self, repository: IProductRepository, task_queue: IProductQueue | None = None) -> None:
        self._repository = repository
        self._task_queue = task_queue

    def list_products(self, limit: int = 100, offset: int = 0, crawl_status: str | None = None) -> list[Product]:
        return self._repository.list_products(limit=limit, offset=offset, crawl_status=crawl_status)

    def count_products(self, crawl_status: str | None = None) -> int:
        return self._repository.count_products(crawl_status=crawl_status)

    def enqueue_product_url(self, remote_url: str) -> Product:
        product = self._repository.create_pending_product(remote_url)
        if self._task_queue is not None:
            self._task_queue.enqueue(CRAWL_EVENT_PRODUCT_URL, product.id)
        return product

    def delete_product(self, product_id: int) -> bool:
        return self._repository.delete_product(product_id)
