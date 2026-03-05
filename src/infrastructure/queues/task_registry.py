from collections.abc import Callable
from importlib import import_module
from typing import Any

from infrastructure.constants.queue import TASK_IMPORT_PATHS


def resolve_task(task_name: str) -> Callable[..., Any]:
    path = TASK_IMPORT_PATHS.get(task_name)
    if path is None:
        raise ValueError(f"Unknown task: {task_name}")

    module_name, attr_name = path.rsplit(".", 1)
    module = import_module(module_name)
    task_fn = getattr(module, attr_name, None)
    if task_fn is None or not callable(task_fn):
        raise ValueError(f"Task not callable: {path}")
    return task_fn
