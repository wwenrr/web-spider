from infrastructure.models.todo import Todo

from core.todos.services.todo_manager import TodoManager

from .runtime import get_todo_manager


def create_todo(title: str) -> None:
    _get_manager().create_todo(title)


def delete_todo(todo_id: int) -> bool:
    return _get_manager().delete_todo(todo_id)


def list_todos() -> list[Todo]:
    return _get_manager().list_todos()


def toggle_todo(todo_id: int) -> None:
    _get_manager().toggle_todo(todo_id)


def update_todo(todo_id: int, title: str) -> bool:
    return _get_manager().update_todo(todo_id, title)


def _get_manager() -> TodoManager:
    return get_todo_manager()
