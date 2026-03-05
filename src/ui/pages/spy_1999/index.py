from ui.data.spy_1999_categories import SPY_1999_CATEGORIES
from ui.data.spy_1999_rankings import SPY_1999_RANKING_CATEGORIES
from ui.pages.spy_1999.cards import render_category_cards
from ui.pages.spy_1999.tabs import SPY_TAB_CATEGORIES, SPY_TAB_RANKINGS, render_spy_tabs

from nicegui import ui


def render_spy_1999_section(initial_tab: str = SPY_TAB_CATEGORIES) -> None:
    active_tab = initial_tab if initial_tab in {SPY_TAB_CATEGORIES, SPY_TAB_RANKINGS} else SPY_TAB_CATEGORIES

    with ui.element("div").classes("spy-root"):
        render_spy_tabs(active_tab)
        if active_tab == SPY_TAB_RANKINGS:
            render_category_cards(SPY_1999_RANKING_CATEGORIES)
            return
        render_category_cards(SPY_1999_CATEGORIES)
