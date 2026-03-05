from collections.abc import Iterable
from typing import Final, cast

from peewee import DoesNotExist

from infrastructure.database import database
from models.todo import Todo, utc_now

EMPTY_TITLE_MESSAGE: Final[str] = "Nội dung không được để trống"


class TodoRepository:
    def list_jobs(self) -> list[Todo]:
        with database:
            return list(Todo.select().order_by(Todo.created_at.desc()))

    def create_job(self, title: str) -> None:
        stripped_title = title.strip()
        if stripped_title == "":
            raise ValueError(EMPTY_TITLE_MESSAGE)

        with database:
            Todo.create(title=stripped_title)

    def get_job(self, job_id: int) -> Todo | None:
        with database:
            try:
                return cast(Todo, Todo.get_by_id(job_id))
            except DoesNotExist:
                return None

    def update_job(self, job_id: int, title: str) -> bool:
        stripped_title = title.strip()
        if stripped_title == "":
            raise ValueError(EMPTY_TITLE_MESSAGE)

        with database:
            updated_rows = cast(
                int,
                Todo.update(title=stripped_title, updated_at=utc_now())
                .where(Todo.id == job_id)
                .execute(),
            )
        return updated_rows > 0

    def toggle_job(self, job_id: int) -> None:
        with database:
            try:
                todo = Todo.get_by_id(job_id)
            except DoesNotExist:
                return

            todo.is_done = not todo.is_done
            todo.save()

    def delete_job(self, job_id: int) -> bool:
        with database:
            deleted_rows = cast(
                int,
                Todo.delete().where(Todo.id == job_id).execute(),
            )
        return deleted_rows > 0

    def delete_completed(self, jobs: Iterable[Todo]) -> None:
        completed_ids = [todo.id for todo in jobs if todo.is_done]
        if not completed_ids:
            return

        with database:
            Todo.delete().where(Todo.id.in_(completed_ids)).execute()


_todo_repository: TodoRepository | None = None


def get_todo_repository() -> TodoRepository:
    global _todo_repository
    if _todo_repository is None:
        _todo_repository = TodoRepository()
    return _todo_repository


def get_job_repository() -> TodoRepository:
    # Backward-compatible alias for current service wiring.
    return get_todo_repository()
