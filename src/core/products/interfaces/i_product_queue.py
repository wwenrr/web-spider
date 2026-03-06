from typing import Protocol


class IProductQueue(Protocol):
    def enqueue(self, task_name: str, *args: object, **kwargs: object) -> None: ...
