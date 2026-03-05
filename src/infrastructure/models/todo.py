from datetime import datetime, timezone
from typing import Final

from peewee import AutoField, BooleanField, CharField, DateTimeField

from infrastructure.models.base import BaseModel
from infrastructure.models.constants import TODO_TABLE_NAME

TODO_TITLE_MAX_LENGTH: Final[int] = 255


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Todo(BaseModel):
    class Meta:
        table_name = TODO_TABLE_NAME

    id = AutoField()
    title = CharField(max_length=TODO_TITLE_MAX_LENGTH)
    is_done = BooleanField(default=False)
    created_at = DateTimeField(default=utc_now)
    updated_at = DateTimeField(default=utc_now)
