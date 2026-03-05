from datetime import datetime


def format_job_time(raw_time: object) -> str:
    if isinstance(raw_time, datetime):
        return raw_time.strftime("%Y-%m-%d %H:%M:%S UTC")

    if isinstance(raw_time, str):
        normalized = raw_time.strip()
        if not normalized:
            return "Unknown update time"

        parsed = _parse_iso_datetime(normalized)
        if parsed is not None:
            return parsed.strftime("%Y-%m-%d %H:%M:%S UTC")

        return normalized

    return "Unknown update time"


def chip_class_for_status(status: str) -> str:
    normalized = status.lower()
    if normalized in {"success", "done", "completed"}:
        return "chip chip--green"
    if normalized in {"failed", "error", "cancelled", "canceled", "dead"}:
        return "chip chip--red"
    if normalized in {"running", "processing", "in_progress", "locked"}:
        return "chip chip--blue"
    return "chip chip--amber"


def _parse_iso_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
