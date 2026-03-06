import json
from typing import Final, cast

from peewee import IntegrityError

from infrastructure.database import database
from infrastructure.models.product import Product, ProductCrawlStatus, utc_now

EMPTY_REMOTE_URL_MESSAGE: Final[str] = "Product URL cannot be empty."
INVALID_REMOTE_URL_MESSAGE: Final[str] = "Product URL must start with http:// or https://."
DUPLICATE_REMOTE_URL_MESSAGE: Final[str] = "Product URL already exists."


class ProductRepository:
    def list_products(self, limit: int = 100) -> list[Product]:
        with database:
            return list(Product.select().order_by(Product.created_at.desc()).limit(limit))

    def get_product(self, product_id: int) -> Product | None:
        with database:
            return Product.get_or_none(Product.id == product_id)

    def create_pending_product(self, remote_url: str) -> Product:
        normalized_remote_url = _normalize_remote_url(remote_url)
        if self.has_remote_url(normalized_remote_url):
            raise ValueError(DUPLICATE_REMOTE_URL_MESSAGE)

        payload = _build_pending_payload(normalized_remote_url)
        with database:
            try:
                return cast(Product, Product.create(**payload))
            except IntegrityError as exc:
                raise ValueError(DUPLICATE_REMOTE_URL_MESSAGE) from exc

    def mark_product_crawl_done(self, product_id: int) -> bool:
        with database:
            updated_rows = cast(
                int,
                Product.update(
                    crawl_status=ProductCrawlStatus.DONE.value,
                    crawl_at=utc_now(),
                    updated_at=utc_now(),
                )
                .where(Product.id == product_id)
                .execute(),
            )
        return updated_rows > 0

    def mark_product_crawl_processing(self, product_id: int) -> bool:
        with database:
            updated_rows = cast(
                int,
                Product.update(
                    crawl_status=ProductCrawlStatus.PROCESSING.value,
                    updated_at=utc_now(),
                )
                .where(Product.id == product_id)
                .execute(),
            )
        return updated_rows > 0

    def has_remote_url(self, remote_url: str) -> bool:
        with database:
            existing = Product.select(Product.id).where(Product.remote_url == remote_url).first()
        return existing is not None

    def delete_product(self, product_id: int) -> bool:
        with database:
            deleted_rows = cast(
                int,
                Product.delete().where(Product.id == product_id).execute(),
            )
        return deleted_rows > 0

    def mark_product_crawl_failed(self, product_id: int) -> bool:
        with database:
            updated_rows = cast(
                int,
                Product.update(
                    crawl_status=ProductCrawlStatus.FAILED.value,
                    updated_at=utc_now(),
                )
                .where(Product.id == product_id)
                .execute(),
            )
        return updated_rows > 0

    def update_product_crawl_result(
        self,
        product_id: int,
        thumbnail: str,
        name: str,
        category: list[str],
        price: str,
        images_url: list[str],
        barcode: str,
        code: str,
        remote_id: str,
        remote_url: str,
        description: str,
    ) -> bool:
        with database:
            updated_rows = cast(
                int,
                Product.update(
                    thumbnail=thumbnail,
                    name=name,
                    category=json.dumps(category, ensure_ascii=False),
                    price=price,
                    images_url=json.dumps(images_url, ensure_ascii=False),
                    barcode=barcode,
                    code=code,
                    remote_id=remote_id,
                    remote_url=remote_url,
                    description=description,
                    crawl_status=ProductCrawlStatus.DONE.value,
                    crawl_at=utc_now(),
                    updated_at=utc_now(),
                )
                .where(Product.id == product_id)
                .execute(),
            )
        return updated_rows > 0


def _normalize_remote_url(raw_remote_url: str) -> str:
    normalized_remote_url = raw_remote_url.strip()
    if normalized_remote_url == "":
        raise ValueError(EMPTY_REMOTE_URL_MESSAGE)
    if not (normalized_remote_url.startswith("http://") or normalized_remote_url.startswith("https://")):
        raise ValueError(INVALID_REMOTE_URL_MESSAGE)
    return normalized_remote_url


def _build_pending_payload(remote_url: str) -> dict[str, object]:
    return {
        "thumbnail": None,
        "name": None,
        "category": json.dumps([]),
        "price": None,
        "images_url": json.dumps([]),
        "barcode": None,
        "code": None,
        "remote_id": None,
        "remote_url": remote_url,
        "description": None,
        "crawl_status": ProductCrawlStatus.PENDING.value,
        "crawl_at": None,
        "updated_at": utc_now(),
    }


_product_repository: ProductRepository | None = None


def get_product_repository() -> ProductRepository:
    global _product_repository
    if _product_repository is None:
        _product_repository = ProductRepository()
    return _product_repository
