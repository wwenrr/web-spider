from nicegui import ui


def render_info_card(title: str, description: str) -> None:
    with ui.card().classes("card"):
        ui.label(title).classes("h2")
        ui.label(description).classes("muted")
