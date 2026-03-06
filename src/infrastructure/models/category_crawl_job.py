from datetime import datetime, timezone
from enum import StrEnum
from typing import Final

from peewee import AutoField, CharField, DateTimeField, IntegerField, TextField

from infrastructure.models.base import BaseModel
from infrastructure.models.constants import CATEGORY_CRAWL_JOB_TABLE_NAME

CATEGORY_CRAWL_TEXT_MAX_LENGTH: Final[int] = 255
CATEGORY_CRAWL_URL_MAX_LENGTH: Final[int] = 2048
CATEGORY_CRAWL_STATUS_MAX_LENGTH: Final[int] = 32
CATEGORY_CRAWL_SITE_KEY_MAX_LENGTH: Final[int] = 64


class CategoryCrawlStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CategoryCrawlJob(BaseModel):
    class Meta:
        table_name = CATEGORY_CRAWL_JOB_TABLE_NAME

    id = AutoField()
    site_key = CharField(max_length=CATEGORY_CRAWL_SITE_KEY_MAX_LENGTH)
    category_name = CharField(max_length=CATEGORY_CRAWL_TEXT_MAX_LENGTH)
    category_url = CharField(max_length=CATEGORY_CRAWL_URL_MAX_LENGTH)
    normalized_category_url = CharField(max_length=CATEGORY_CRAWL_URL_MAX_LENGTH)
    crawl_status = CharField(max_length=CATEGORY_CRAWL_STATUS_MAX_LENGTH, default=CategoryCrawlStatus.PENDING.value)
    total_products = IntegerField(null=True)
    products_per_page = IntegerField(null=True)
    total_pages = IntegerField(null=True)
    enqueued_products_count = IntegerField(null=True)
    crawl_at = DateTimeField(null=True)
    error_message = TextField(null=True)
    created_at = DateTimeField(default=utc_now)
    updated_at = DateTimeField(default=utc_now)
