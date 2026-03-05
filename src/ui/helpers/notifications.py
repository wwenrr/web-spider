from nicegui import ui


def show_error(message: str) -> None:
    ui.notify(message, color="negative")


def show_success(message: str) -> None:
    ui.notify(message, color="positive")
