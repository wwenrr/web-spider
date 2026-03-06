from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
import sqlite3
from typing import Final

from infrastructure.constants.db import DB_DIR_PATH

DEFAULT_QUEUE_DB_PATH: Final[Path] = DB_DIR_PATH / "pybgworker.db"
STATUS_DONE: Final[set[str]] = {"success", "done", "completed"}
STATUS_FAILED: Final[set[str]] = {"failed", "error", "cancelled", "canceled", "dead"}
STATUS_PENDING: Final[set[str]] = {"pending", "queued", "scheduled", "retry"}
STATUS_RUNNING: Final[set[str]] = {"running", "processing", "in_progress", "locked"}
QUEUE_STATUS_GROUPS: Final[dict[str, set[str]]] = {
    "pending": STATUS_PENDING,
    "running": STATUS_RUNNING,
    "done": STATUS_DONE,
    "failed": STATUS_FAILED,
}


@dataclass(frozen=True)
class QueueJob:
    id: str
    name: str
    status: str
    attempt: int
    max_retries: int
    updated_at: str | None
    created_at: str | None
    finished_at: str | None
    last_error: str | None


@dataclass(frozen=True)
class QueueStats:
    total: int
    pending: int
    running: int
    done: int
    failed: int


def get_queue_stats() -> QueueStats:
    status_counts = _fetch_status_counts()
    total = sum(status_counts.values())
    pending = sum(count for status, count in status_counts.items() if status in STATUS_PENDING)
    running = sum(count for status, count in status_counts.items() if status in STATUS_RUNNING)
    done = sum(count for status, count in status_counts.items() if status in STATUS_DONE)
    failed = sum(count for status, count in status_counts.items() if status in STATUS_FAILED)
    return QueueStats(total=total, pending=pending, running=running, done=done, failed=failed)


def list_queue_jobs(limit: int = 50, offset: int = 0, status_filter: str | None = None) -> list[QueueJob]:
    db_path = _resolve_queue_db_path()
    if not db_path.exists():
        return []

    where_clause, params = _build_status_filter_clause(status_filter)
    rows = _query(
        db_path,
        """
        SELECT id, name, status, attempt, max_retries, updated_at, created_at, finished_at, last_error
        FROM tasks
        """
        + where_clause
        + """
        ORDER BY datetime(created_at) DESC, created_at DESC
        LIMIT ?
        OFFSET ?
        """,
        (*params, limit, offset),
    )
    return [
        QueueJob(
            id=str(row[0] or ""),
            name=str(row[1] or "unnamed"),
            status=str(row[2] or "unknown").lower(),
            attempt=int(row[3] or 0),
            max_retries=int(row[4] or 0),
            updated_at=_normalize_timestamp(row[5]),
            created_at=_normalize_timestamp(row[6]),
            finished_at=_normalize_timestamp(row[7]),
            last_error=str(row[8]) if row[8] else None,
        )
        for row in rows
    ]


def count_queue_jobs(status_filter: str | None = None) -> int:
    db_path = _resolve_queue_db_path()
    if not db_path.exists():
        return 0

    where_clause, params = _build_status_filter_clause(status_filter)
    rows = _query(
        db_path,
        "SELECT COUNT(*) FROM tasks " + where_clause,
        params,
    )
    if not rows:
        return 0
    return int(rows[0][0] or 0)


def _fetch_status_counts() -> dict[str, int]:
    db_path = _resolve_queue_db_path()
    if not db_path.exists():
        return {}

    rows = _query(
        db_path,
        "SELECT lower(coalesce(status, 'unknown')) AS status, COUNT(*) AS total FROM tasks GROUP BY status",
        (),
    )
    return {str(row[0]): int(row[1]) for row in rows}


def _query(db_path: Path, sql: str, params: tuple[object, ...]) -> list[tuple]:
    try:
        with sqlite3.connect(str(db_path)) as conn:
            return conn.execute(sql, params).fetchall()
    except sqlite3.Error:
        return []


def _build_status_filter_clause(status_filter: str | None) -> tuple[str, tuple[object, ...]]:
    if status_filter is None:
        return "", ()

    normalized_filter = status_filter.strip().lower()
    statuses = QUEUE_STATUS_GROUPS.get(normalized_filter)
    if not statuses:
        return "", ()

    placeholders = ", ".join("?" for _ in statuses)
    return f"WHERE lower(coalesce(status, 'unknown')) IN ({placeholders}) ", tuple(sorted(statuses))


def _resolve_queue_db_path() -> Path:
    configured = os.environ.get("PYBGWORKER_DB")
    if configured:
        return Path(configured)
    return DEFAULT_QUEUE_DB_PATH


def _normalize_timestamp(value: object) -> str | None:
    if value is None:
        return None

    as_text = str(value).strip()
    if not as_text:
        return None

    parsed = _parse_iso_datetime(as_text)
    if parsed is None:
        return as_text
    return parsed.isoformat()


def _parse_iso_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
