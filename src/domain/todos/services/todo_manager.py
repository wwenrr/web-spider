from domain.todos.interfaces import ITodoQueue, ITodoRepository
from domain.todos.constants import AUDIT_EVENT_JOB_CREATED
from models.todo import Todo


class TodoManager:
    def __init__(self, repository: ITodoRepository, task_queue: ITodoQueue | None = None) -> None:
        self._repository = repository
        self._task_queue = task_queue

    def list_todos(self) -> list[Todo]:
        return self._repository.list_todos()

    def create_todo(self, title: str) -> None:
        self._repository.create_todo(title)
        if self._task_queue is not None:
            self._task_queue.enqueue(AUDIT_EVENT_JOB_CREATED, title)

    def update_todo(self, todo_id: int, title: str) -> bool:
        return self._repository.update_todo(todo_id, title)

    def toggle_todo(self, todo_id: int) -> None:
        self._repository.toggle_todo(todo_id)

    def delete_todo(self, todo_id: int) -> bool:
        return self._repository.delete_todo(todo_id)
