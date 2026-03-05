from pathlib import Path
from typing import Final

_THEME_PATH: Final[Path] = Path(__file__).resolve().with_name("theme.css")
_CUSTOM_PATH: Final[Path] = Path(__file__).resolve().with_name("custom.css")


def build_css() -> str:
    return f"{_THEME_PATH.read_text(encoding='utf-8')}\n\n{_CUSTOM_PATH.read_text(encoding='utf-8')}"
