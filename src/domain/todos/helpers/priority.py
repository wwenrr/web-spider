def get_priority(label: str) -> int:
    priorities = {"high": 3, "medium": 2, "low": 1}
    return priorities.get(label.lower(), 1)
