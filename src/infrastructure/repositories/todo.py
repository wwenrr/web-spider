from collections.abc import Iterable
from typing import Final, cast

from peewee import DoesNotExist

from infrastructure.database import database
from models.todo import Todo, utc_now

EMPTY_TITLE_MESSAGE: Final[str] = "Nội dung không được để trống"


class TodoRepository:
    def list_todos(self) -> list[Todo]:
        with database:
            return list(Todo.select().order_by(Todo.created_at.desc()))

    def create_todo(self, title: str) -> None:
        stripped_title = title.strip()
        if stripped_title == "":
            raise ValueError(EMPTY_TITLE_MESSAGE)

        with database:
            Todo.create(title=stripped_title)

    def get_todo(self, todo_id: int) -> Todo | None:
        with database:
            try:
                return cast(Todo, Todo.get_by_id(todo_id))
            except DoesNotExist:
                return None

    def update_todo(self, todo_id: int, title: str) -> bool:
        stripped_title = title.strip()
        if stripped_title == "":
            raise ValueError(EMPTY_TITLE_MESSAGE)

        with database:
            updated_rows = cast(
                int,
                Todo.update(title=stripped_title, updated_at=utc_now())
                .where(Todo.id == todo_id)
                .execute(),
            )
        return updated_rows > 0

    def toggle_todo(self, todo_id: int) -> None:
        with database:
            try:
                todo = Todo.get_by_id(todo_id)
            except DoesNotExist:
                return

            todo.is_done = not todo.is_done
            todo.save()

    def delete_todo(self, todo_id: int) -> bool:
        with database:
            deleted_rows = cast(
                int,
                Todo.delete().where(Todo.id == todo_id).execute(),
            )
        return deleted_rows > 0

    def delete_completed_todos(self, todos: Iterable[Todo]) -> None:
        completed_ids = [todo.id for todo in todos if todo.is_done]
        if not completed_ids:
            return

        with database:
            Todo.delete().where(Todo.id.in_(completed_ids)).execute()

    def list_jobs(self) -> list[Todo]:
        return self.list_todos()

    def create_job(self, title: str) -> None:
        self.create_todo(title)

    def get_job(self, job_id: int) -> Todo | None:
        return self.get_todo(job_id)

    def update_job(self, job_id: int, title: str) -> bool:
        return self.update_todo(job_id, title)

    def toggle_job(self, job_id: int) -> None:
        self.toggle_todo(job_id)

    def delete_job(self, job_id: int) -> bool:
        return self.delete_todo(job_id)

    def delete_completed(self, jobs: Iterable[Todo]) -> None:
        self.delete_completed_todos(jobs)


_todo_repository: TodoRepository | None = None


def get_todo_repository() -> TodoRepository:
    global _todo_repository
    if _todo_repository is None:
        _todo_repository = TodoRepository()
    return _todo_repository


def get_job_repository() -> TodoRepository:
    # Backward-compatible alias for current service wiring.
    return get_todo_repository()
