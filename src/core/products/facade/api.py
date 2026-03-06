from core.products.services import ProductManager
from infrastructure.models.product import Product

from .runtime import get_product_manager


def list_products(limit: int = 100) -> list[Product]:
    return _get_manager().list_products(limit=limit)


def enqueue_product_url(remote_url: str) -> Product:
    return _get_manager().enqueue_product_url(remote_url)


def delete_product(product_id: int) -> bool:
    return _get_manager().delete_product(product_id)


def _get_manager() -> ProductManager:
    return get_product_manager()
