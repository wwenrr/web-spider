from typing import Protocol


class ITodoQueue(Protocol):
    def enqueue(self, task_name: str, *args: object, **kwargs: object) -> None: ...
