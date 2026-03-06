from core.products.services import ProductManager

_product_manager: ProductManager | None = None


def configure_product_manager(product_manager: ProductManager) -> None:
    global _product_manager
    _product_manager = product_manager


def get_product_manager() -> ProductManager:
    if _product_manager is None:
        raise RuntimeError("ProductManager is not configured")
    return _product_manager
