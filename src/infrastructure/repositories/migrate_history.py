from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(slots=True)
class MigrationRecord:
    version: str
    applied_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MigrateHistoryRepository:
    def __init__(self) -> None:
        self._records: list[MigrationRecord] = []

    def list_records(self) -> list[MigrationRecord]:
        return list(self._records)

    def add_record(self, version: str) -> None:
        self._records.append(MigrationRecord(version=version))


_migrate_history_repository: MigrateHistoryRepository | None = None


def get_migrate_history_repository() -> MigrateHistoryRepository:
    global _migrate_history_repository
    if _migrate_history_repository is None:
        _migrate_history_repository = MigrateHistoryRepository()
    return _migrate_history_repository
