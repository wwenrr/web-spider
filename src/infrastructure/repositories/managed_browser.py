from pathlib import Path
from typing import Final, cast

from peewee import IntegrityError

from infrastructure.database import database
from infrastructure.models.managed_browser import ManagedBrowser, ManagedBrowserStatus, utc_now

DEFAULT_MANAGED_BROWSER_HOST: Final[str] = "127.0.0.1"
DEFAULT_MANAGED_BROWSER_PORT: Final[int] = 9333
DEFAULT_MANAGED_BROWSER_TYPE: Final[str] = "chrome"
DEFAULT_MANAGED_BROWSER_PROFILE_DIR: Final[str] = "/tmp/web-spider-managed-browser"
EMPTY_HOST_MESSAGE: Final[str] = "Host cannot be empty."
EMPTY_PROFILE_DIR_MESSAGE: Final[str] = "User data directory cannot be empty."
INVALID_PORT_MESSAGE: Final[str] = "Port must be within 1-65535."
BROWSER_NAME_EXISTS_MESSAGE: Final[str] = "Managed browser name already exists."
BROWSER_PORT_EXISTS_MESSAGE: Final[str] = "Managed browser port already exists."
BROWSER_RUNNING_DELETE_MESSAGE: Final[str] = "Stop the browser before deleting this config."
SPIDER_BROWSER_PREFIXES: Final[tuple[str, ...]] = (
    "Orb",
    "Silk",
    "Echo",
    "Thread",
    "Shadow",
    "Signal",
    "Swift",
    "Velvet",
)
SPIDER_BROWSER_SUFFIXES: Final[tuple[str, ...]] = (
    "Spinner",
    "Crawler",
    "Weaver",
    "Hunter",
    "Scout",
    "Runner",
    "Watcher",
    "Stalker",
)


class ManagedBrowserRepository:
    def list_browsers(self) -> list[ManagedBrowser]:
        with database:
            return list(ManagedBrowser.select().order_by(ManagedBrowser.created_at.desc()))

    def get_browser(self, browser_id: int) -> ManagedBrowser | None:
        with database:
            return ManagedBrowser.get_or_none(ManagedBrowser.id == browser_id)

    def get_active_browser(self) -> ManagedBrowser | None:
        with database:
            return (
                ManagedBrowser.select()
                .where(ManagedBrowser.is_active == True)
                .order_by(ManagedBrowser.updated_at.desc(), ManagedBrowser.id.desc())
                .first()
            )

    def ensure_default_active_browser(self, *, headless: bool) -> ManagedBrowser:
        active_browser = self.get_active_browser()
        if active_browser is not None:
            return active_browser

        with database.atomic():
            active_browser = self.get_active_browser()
            if active_browser is not None:
                return active_browser
            self._deactivate_other_browsers()
            return cast(
                ManagedBrowser,
                ManagedBrowser.create(
                    name=_generate_browser_name(),
                    browser_type=DEFAULT_MANAGED_BROWSER_TYPE,
                    host=DEFAULT_MANAGED_BROWSER_HOST,
                    port=DEFAULT_MANAGED_BROWSER_PORT,
                    executable_path=None,
                    user_data_dir=DEFAULT_MANAGED_BROWSER_PROFILE_DIR,
                    headless=headless,
                    launch_args=None,
                    is_active=True,
                    status=ManagedBrowserStatus.STOPPED.value,
                    pid=None,
                    last_started_at=None,
                    last_seen_at=None,
                    notes="Auto-created fallback browser.",
                    error_message=None,
                    updated_at=utc_now(),
                ),
            )

    def create_browser(
        self,
        name: str,
        browser_type: str,
        host: str,
        port: int,
        executable_path: str | None,
        user_data_dir: str,
        headless: bool,
        launch_args: str | None,
        is_active: bool,
        notes: str | None,
    ) -> None:
        payload = _build_validated_payload(
            name=name,
            browser_type=browser_type,
            host=host,
            port=port,
            executable_path=executable_path,
            user_data_dir=user_data_dir,
            headless=headless,
            launch_args=launch_args,
            is_active=is_active,
            notes=notes,
            exclude_id=None,
        )
        with database.atomic():
            if is_active:
                self._deactivate_other_browsers()
            try:
                ManagedBrowser.create(**payload)
            except IntegrityError as exc:
                raise _translate_integrity_error(exc) from exc

    def update_browser(
        self,
        browser_id: int,
        name: str,
        browser_type: str,
        host: str,
        port: int,
        executable_path: str | None,
        user_data_dir: str,
        headless: bool,
        launch_args: str | None,
        is_active: bool,
        notes: str | None,
    ) -> bool:
        payload = _build_validated_payload(
            name=name,
            browser_type=browser_type,
            host=host,
            port=port,
            executable_path=executable_path,
            user_data_dir=user_data_dir,
            headless=headless,
            launch_args=launch_args,
            is_active=is_active,
            notes=notes,
            exclude_id=browser_id,
        )
        with database.atomic():
            if is_active:
                self._deactivate_other_browsers(exclude_id=browser_id)
            try:
                updated_rows = cast(
                    int,
                    ManagedBrowser.update(**payload, updated_at=utc_now())
                    .where(ManagedBrowser.id == browser_id)
                    .execute(),
                )
            except IntegrityError as exc:
                raise _translate_integrity_error(exc) from exc
        return updated_rows > 0

    def delete_browser(self, browser_id: int) -> bool:
        browser = self.get_browser(browser_id)
        if browser is not None and browser.status == ManagedBrowserStatus.RUNNING.value:
            raise ValueError(BROWSER_RUNNING_DELETE_MESSAGE)

        with database:
            deleted_rows = cast(
                int,
                ManagedBrowser.delete().where(ManagedBrowser.id == browser_id).execute(),
            )
        return deleted_rows > 0

    def claim_starting(self, browser_id: int) -> bool:
        with database:
            updated_rows = cast(
                int,
                ManagedBrowser.update(
                    status=ManagedBrowserStatus.STARTING.value,
                    error_message=None,
                    updated_at=utc_now(),
                )
                .where(
                    (ManagedBrowser.id == browser_id)
                    & (ManagedBrowser.status != ManagedBrowserStatus.STARTING.value)
                )
                .execute(),
            )
        return updated_rows > 0

    def mark_running(self, browser_id: int, pid: int | None) -> bool:
        with database:
            updated_rows = cast(
                int,
                ManagedBrowser.update(
                    status=ManagedBrowserStatus.RUNNING.value,
                    pid=pid,
                    last_started_at=utc_now(),
                    last_seen_at=utc_now(),
                    error_message=None,
                    updated_at=utc_now(),
                )
                .where(ManagedBrowser.id == browser_id)
                .execute(),
            )
        return updated_rows > 0

    def touch_seen(self, browser_id: int) -> bool:
        with database:
            updated_rows = cast(
                int,
                ManagedBrowser.update(
                    last_seen_at=utc_now(),
                    updated_at=utc_now(),
                )
                .where(ManagedBrowser.id == browser_id)
                .execute(),
            )
        return updated_rows > 0

    def mark_stopped(self, browser_id: int) -> bool:
        with database:
            updated_rows = cast(
                int,
                ManagedBrowser.update(
                    status=ManagedBrowserStatus.STOPPED.value,
                    pid=None,
                    error_message=None,
                    updated_at=utc_now(),
                )
                .where(ManagedBrowser.id == browser_id)
                .execute(),
            )
        return updated_rows > 0

    def mark_failed(self, browser_id: int, error_message: str) -> bool:
        with database:
            updated_rows = cast(
                int,
                ManagedBrowser.update(
                    status=ManagedBrowserStatus.FAILED.value,
                    error_message=error_message.strip() or "Managed browser failed.",
                    updated_at=utc_now(),
                )
                .where(ManagedBrowser.id == browser_id)
                .execute(),
            )
        return updated_rows > 0

    def _deactivate_other_browsers(self, exclude_id: int | None = None) -> None:
        query = ManagedBrowser.update(is_active=False, updated_at=utc_now())
        if exclude_id is not None:
            query = query.where(ManagedBrowser.id != exclude_id)
        query.execute()


def get_managed_browser_repository() -> ManagedBrowserRepository:
    global _managed_browser_repository
    if _managed_browser_repository is None:
        _managed_browser_repository = ManagedBrowserRepository()
    return _managed_browser_repository


def _build_validated_payload(
    *,
    name: str,
    browser_type: str,
    host: str,
    port: int,
    executable_path: str | None,
    user_data_dir: str,
    headless: bool,
    launch_args: str | None,
    is_active: bool,
    notes: str | None,
    exclude_id: int | None,
) -> dict[str, object]:
    normalized_host = host.strip()
    if normalized_host == "":
        raise ValueError(EMPTY_HOST_MESSAGE)

    if port < 1 or port > 65535:
        raise ValueError(INVALID_PORT_MESSAGE)

    normalized_profile_dir = user_data_dir.strip()
    if normalized_profile_dir == "":
        raise ValueError(EMPTY_PROFILE_DIR_MESSAGE)

    normalized_type = browser_type.strip() or DEFAULT_MANAGED_BROWSER_TYPE
    normalized_name = _normalize_browser_name(name=name, exclude_id=exclude_id)

    return {
        "name": normalized_name,
        "browser_type": normalized_type,
        "host": normalized_host,
        "port": port,
        "executable_path": _optional_text(executable_path),
        "user_data_dir": str(Path(normalized_profile_dir).expanduser()),
        "headless": headless,
        "launch_args": _optional_text(launch_args),
        "is_active": is_active,
        "notes": _optional_text(notes),
    }


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    if normalized == "":
        return None
    return normalized


def _translate_integrity_error(error: IntegrityError) -> ValueError:
    message = str(error).lower()
    if "managed_browser.name" in message or "name" in message:
        return ValueError(BROWSER_NAME_EXISTS_MESSAGE)
    if "managed_browser.port" in message or "port" in message:
        return ValueError(BROWSER_PORT_EXISTS_MESSAGE)
    return ValueError("Managed browser could not be saved.")


def _normalize_browser_name(*, name: str, exclude_id: int | None) -> str:
    normalized_name = name.strip()
    if normalized_name != "":
        return normalized_name
    return _generate_browser_name(exclude_id=exclude_id)


def _generate_browser_name(exclude_id: int | None = None) -> str:
    for prefix in SPIDER_BROWSER_PREFIXES:
        for suffix in SPIDER_BROWSER_SUFFIXES:
            candidate = f"{prefix} {suffix}"
            if not _name_exists(candidate, exclude_id=exclude_id):
                return candidate

    sequence = 1
    while True:
        candidate = f"{SPIDER_BROWSER_PREFIXES[0]} {SPIDER_BROWSER_SUFFIXES[0]} {sequence}"
        if not _name_exists(candidate, exclude_id=exclude_id):
            return candidate
        sequence += 1


def _name_exists(name: str, *, exclude_id: int | None) -> bool:
    query = ManagedBrowser.select(ManagedBrowser.id).where(ManagedBrowser.name == name)
    if exclude_id is not None:
        query = query.where(ManagedBrowser.id != exclude_id)
    return query.exists()


_managed_browser_repository: ManagedBrowserRepository | None = None
