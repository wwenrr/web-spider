from domain.todos.interfaces import ITodoRepository
from models.todo import Todo


class TodoManager:
    def __init__(self, repository: ITodoRepository) -> None:
        self._repository = repository

    def list_todos(self) -> list[Todo]:
        return self._repository.list_todos()

    def create_todo(self, title: str) -> None:
        self._repository.create_todo(title)

    def update_todo(self, todo_id: int, title: str) -> bool:
        return self._repository.update_todo(todo_id, title)

    def toggle_todo(self, todo_id: int) -> None:
        self._repository.toggle_todo(todo_id)

    def delete_todo(self, todo_id: int) -> bool:
        return self._repository.delete_todo(todo_id)
