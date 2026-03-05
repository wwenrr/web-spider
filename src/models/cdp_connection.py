from datetime import datetime, timezone
from typing import Final

from peewee import AutoField, BooleanField, CharField, DateTimeField, IntegerField, TextField

from models.base import BaseModel
from models.constants import CDP_CONNECTION_TABLE_NAME

CDP_CONNECTION_NAME_MAX_LENGTH: Final[int] = 120
CDP_CONNECTION_HOST_MAX_LENGTH: Final[int] = 255
CDP_CONNECTION_BROWSER_MAX_LENGTH: Final[int] = 32
CDP_CONNECTION_PATH_MAX_LENGTH: Final[int] = 255
CDP_CONNECTION_USERNAME_MAX_LENGTH: Final[int] = 255
CDP_CONNECTION_PASSWORD_MAX_LENGTH: Final[int] = 255


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CdpConnection(BaseModel):
    class Meta:
        table_name = CDP_CONNECTION_TABLE_NAME

    id = AutoField()
    name = CharField(max_length=CDP_CONNECTION_NAME_MAX_LENGTH)
    host = CharField(max_length=CDP_CONNECTION_HOST_MAX_LENGTH)
    port = IntegerField()
    browser = CharField(max_length=CDP_CONNECTION_BROWSER_MAX_LENGTH, default="chrome")
    ws_path = CharField(max_length=CDP_CONNECTION_PATH_MAX_LENGTH, default="/devtools/browser")
    username = CharField(max_length=CDP_CONNECTION_USERNAME_MAX_LENGTH, null=True)
    password = CharField(max_length=CDP_CONNECTION_PASSWORD_MAX_LENGTH, null=True)
    is_active = BooleanField(default=True)
    notes = TextField(null=True)
    created_at = DateTimeField(default=utc_now)
    updated_at = DateTimeField(default=utc_now)
