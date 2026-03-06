from datetime import datetime, timezone
from enum import StrEnum
from typing import Final

from peewee import AutoField, BooleanField, CharField, DateTimeField, IntegerField, TextField

from infrastructure.models.base import BaseModel
from infrastructure.models.constants import MANAGED_BROWSER_TABLE_NAME

MANAGED_BROWSER_NAME_MAX_LENGTH: Final[int] = 120
MANAGED_BROWSER_TYPE_MAX_LENGTH: Final[int] = 32
MANAGED_BROWSER_HOST_MAX_LENGTH: Final[int] = 255
MANAGED_BROWSER_PATH_MAX_LENGTH: Final[int] = 1024
MANAGED_BROWSER_STATUS_MAX_LENGTH: Final[int] = 32
MANAGED_BROWSER_EXECUTABLE_PATH_MAX_LENGTH: Final[int] = 1024


class ManagedBrowserStatus(StrEnum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    FAILED = "failed"



def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ManagedBrowser(BaseModel):
    class Meta:
        table_name = MANAGED_BROWSER_TABLE_NAME

    id = AutoField()
    name = CharField(max_length=MANAGED_BROWSER_NAME_MAX_LENGTH, unique=True)
    browser_type = CharField(max_length=MANAGED_BROWSER_TYPE_MAX_LENGTH, default="chrome")
    host = CharField(max_length=MANAGED_BROWSER_HOST_MAX_LENGTH, default="127.0.0.1")
    port = IntegerField(unique=True)
    executable_path = CharField(max_length=MANAGED_BROWSER_EXECUTABLE_PATH_MAX_LENGTH, null=True)
    user_data_dir = CharField(max_length=MANAGED_BROWSER_PATH_MAX_LENGTH)
    headless = BooleanField(default=False)
    launch_args = TextField(null=True)
    is_active = BooleanField(default=True)
    status = CharField(max_length=MANAGED_BROWSER_STATUS_MAX_LENGTH, default=ManagedBrowserStatus.STOPPED.value)
    pid = IntegerField(null=True)
    last_started_at = DateTimeField(null=True)
    last_seen_at = DateTimeField(null=True)
    notes = TextField(null=True)
    error_message = TextField(null=True)
    created_at = DateTimeField(default=utc_now)
    updated_at = DateTimeField(default=utc_now)
