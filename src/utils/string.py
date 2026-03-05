import re


def slugify(text: str) -> str:
    lowered = text.strip().lower()
    lowered = re.sub(r"[^a-z0-9\s-]", "", lowered)
    return re.sub(r"[\s-]+", "-", lowered).strip("-")


def sanitize(text: str) -> str:
    return " ".join(text.strip().split())
