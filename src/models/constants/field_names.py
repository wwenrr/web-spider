from typing import Final

TODO_FIELD_NAMES: Final[tuple[str, ...]] = ("id", "title", "is_done", "created_at", "updated_at")
CDP_CONNECTION_FIELD_NAMES: Final[tuple[str, ...]] = (
    "id",
    "name",
    "host",
    "port",
    "browser",
    "ws_path",
    "username",
    "password",
    "is_active",
    "notes",
    "created_at",
    "updated_at",
)
