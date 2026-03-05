from pathlib import Path
from typing import Final

_THEME_PATH: Final[Path] = Path(__file__).resolve().with_name("theme.css")
_STYLES_DIR: Final[Path] = Path(__file__).resolve().with_name("styles")
_STYLE_ORDER: Final[tuple[str, ...]] = (
    "00_reset.css",
    "01_base.css",
    "02_quasar_bridge.css",
    "10_layout.css",
    "20_todo.css",
    "30_cdp.css",
    "35_spy.css",
    "40_monitor.css",
    "50_components.css",
    "90_responsive.css",
)


def build_css() -> str:
    css_parts = [_THEME_PATH.read_text(encoding="utf-8")]
    for style_name in _STYLE_ORDER:
        style_path = _STYLES_DIR / style_name
        css_parts.append(style_path.read_text(encoding="utf-8"))
    return "\n\n".join(css_parts)
