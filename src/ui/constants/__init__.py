import base64
from pathlib import Path
from typing import Final

from .colors import (
    ACCENT,
    ACCENT_BG,
    ACCENT_HOVER,
    BG_ALT,
    BORDER,
    FONT,
    PAGE_TITLE,
    SIDEBAR_W,
    TEXT,
    TEXT_2,
    TEXT_3,
)
from .routes import (
    ROUTE_CDP_CONNECTIONS,
    ROUTE_DASHBOARD,
    ROUTE_MONITOR,
    ROUTE_ROOT,
    ROUTE_TODO,
)
from .table_ids import TABLE_ID_JOBS

__all__ = [
    "ACCENT",
    "ACCENT_BG",
    "ACCENT_HOVER",
    "BG_ALT",
    "BORDER",
    "FONT",
    "PAGE_TITLE",
    "ROUTE_CDP_CONNECTIONS",
    "ROUTE_DASHBOARD",
    "ROUTE_MONITOR",
    "ROUTE_ROOT",
    "ROUTE_TODO",
    "SIDEBAR_LOGO_HTML",
    "SIDEBAR_W",
    "TABLE_ID_JOBS",
    "TEXT",
    "TEXT_2",
    "TEXT_3",
    "build_favicon_head_html",
]

_LOGO_PATH: Final[Path] = Path(__file__).resolve().parents[1] / "static" / "logo.png"
STATIC_LOGO_URL: Final[str] = "/static/logo.png"

FAVICON_DATA_URI: Final[str | None] = (
    f"data:image/png;base64,{base64.b64encode(_LOGO_PATH.read_bytes()).decode('ascii')}"
    if _LOGO_PATH.exists()
    else None
)

SIDEBAR_LOGO_HTML: Final[str]
if _LOGO_PATH.exists():
    SIDEBAR_LOGO_HTML = (
        f'<img src="{STATIC_LOGO_URL}" '
        'alt="Web Spider logo" width="88" height="88">'
    )
else:
    SIDEBAR_LOGO_HTML = (
        '<svg viewBox="0 0 128 128" fill="none" width="88" height="88" aria-label="Web Spider logo">'
        f'<polygon points="64,8 109,34 109,94 64,120 19,94 19,34" fill="{ACCENT}"/>'
        f'<polygon points="64,18 100,39 100,89 64,110 28,89 28,39" fill="{ACCENT_HOVER}"/>'
        "</svg>"
    )


def build_favicon_head_html() -> str:
    if not FAVICON_DATA_URI:
        return ""
    return (
        "<script>"
        "(function(){"
        "const rels=['icon','shortcut icon','apple-touch-icon'];"
        "rels.forEach(r=>document.querySelectorAll(`link[rel=\\\"${r}\\\"]`).forEach(el=>el.remove()));"
        "const mk=(rel)=>{const l=document.createElement('link');l.rel=rel;l.href='"
        f"{FAVICON_DATA_URI}"
        "';l.type='image/png';document.head.appendChild(l);};"
        "mk('icon');mk('shortcut icon');mk('apple-touch-icon');"
        "})();"
        "</script>"
    )
