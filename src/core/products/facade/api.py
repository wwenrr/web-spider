from core.products.services import ProductManager
from infrastructure.models.product import Product

from .runtime import get_product_manager


def list_products(limit: int = 100, offset: int = 0, crawl_status: str | None = None) -> list[Product]:
    return _get_manager().list_products(limit=limit, offset=offset, crawl_status=crawl_status)


def count_products(crawl_status: str | None = None) -> int:
    return _get_manager().count_products(crawl_status=crawl_status)


def enqueue_product_url(remote_url: str) -> Product:
    return _get_manager().enqueue_product_url(remote_url)


def delete_product(product_id: int) -> bool:
    return _get_manager().delete_product(product_id)


def _get_manager() -> ProductManager:
    return get_product_manager()
