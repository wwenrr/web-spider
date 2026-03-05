from dataclasses import dataclass


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
