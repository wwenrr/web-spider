from typing import Protocol

from infrastructure.models.product import Product


class IProductRepository(Protocol):
    def list_products(self, limit: int = 100) -> list[Product]: ...

    def create_pending_product(self, remote_url: str) -> Product: ...

    def delete_product(self, product_id: int) -> bool: ...
