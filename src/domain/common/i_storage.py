from typing import Protocol


class IStorage(Protocol):
    def save(self, payload: dict) -> None: ...
