from datetime import datetime, timezone
from enum import StrEnum
from typing import Final

from peewee import AutoField, CharField, DateTimeField, TextField

from infrastructure.models.base import BaseModel
from infrastructure.models.constants import PRODUCT_TABLE_NAME

PRODUCT_TEXT_MAX_LENGTH: Final[int] = 255
PRODUCT_URL_MAX_LENGTH: Final[int] = 2048
PRODUCT_STATUS_MAX_LENGTH: Final[int] = 32


class ProductCrawlStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Product(BaseModel):
    class Meta:
        table_name = PRODUCT_TABLE_NAME

    id = AutoField()
    thumbnail = CharField(max_length=PRODUCT_URL_MAX_LENGTH, null=True)
    name = CharField(max_length=PRODUCT_TEXT_MAX_LENGTH, null=True)
    category = TextField(default="[]")
    price = CharField(max_length=PRODUCT_TEXT_MAX_LENGTH, null=True)
    images_url = TextField(default="[]")
    barcode = CharField(max_length=PRODUCT_TEXT_MAX_LENGTH, null=True)
    code = CharField(max_length=PRODUCT_TEXT_MAX_LENGTH, null=True)
    remote_id = CharField(max_length=PRODUCT_TEXT_MAX_LENGTH, null=True)
    remote_url = CharField(max_length=PRODUCT_URL_MAX_LENGTH, unique=True)
    description = TextField(null=True)
    crawl_status = CharField(max_length=PRODUCT_STATUS_MAX_LENGTH, default=ProductCrawlStatus.PENDING.value)
    crawl_at = DateTimeField(null=True)
    created_at = DateTimeField(default=utc_now)
    updated_at = DateTimeField(default=utc_now)
