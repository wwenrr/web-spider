from .todo_manager import TodoManager

_todo_manager: TodoManager | None = None


def configure_todo_manager(todo_manager: TodoManager) -> None:
    global _todo_manager
    _todo_manager = todo_manager


def get_todo_manager() -> TodoManager:
    if _todo_manager is None:
        raise RuntimeError("TodoManager is not configured")
    return _todo_manager
