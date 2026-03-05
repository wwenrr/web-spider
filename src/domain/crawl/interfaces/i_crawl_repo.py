from typing import Protocol


class ICrawlRepo(Protocol):
    def save_result(self, payload: dict) -> None: ...
