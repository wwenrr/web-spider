from collections.abc import Callable

from core.todos.facade import create_todo, delete_todo, toggle_todo, update_todo
from ui.helpers import show_error, show_success


def handle_create_todo(
    raw_title: str | None,
    refresh_list: Callable[[], None],
    clear_input: Callable[[], None],
) -> None:
    title = (raw_title or "").strip()
    try:
        create_todo(title)
    except ValueError as err:
        show_error(str(err))
        return

    clear_input()
    refresh_list()
    show_success("Todo created")


def handle_update_todo(todo_id: int, raw_title: str | None, refresh_list: Callable[[], None]) -> None:
    title = (raw_title or "").strip()
    try:
        updated = update_todo(todo_id, title)
    except ValueError as err:
        show_error(str(err))
        return

    if not updated:
        show_error("Todo no longer exists.")
        refresh_list()
        return

    refresh_list()
    show_success("Todo updated")


def handle_toggle_todo(todo_id: int, refresh_list: Callable[[], None]) -> None:
    toggle_todo(todo_id)
    refresh_list()
    show_success("Todo status updated")


def handle_delete_todo(todo_id: int, refresh_list: Callable[[], None]) -> None:
    deleted = delete_todo(todo_id)
    if not deleted:
        show_error("Todo no longer exists.")
        refresh_list()
        return

    refresh_list()
    show_success("Todo deleted")
