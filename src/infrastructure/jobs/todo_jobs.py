from pathlib import Path
from typing import Final
import os
import time

from pybgworker import utils as bg_utils
from pybgworker.task import task

from infrastructure.constants.db import DB_DIR_PATH
from infrastructure.constants.queue import TASK_LOG_TODO_CREATED

DB_DIR: Final[Path] = DB_DIR_PATH
DB_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("PYBGWORKER_DB", str(DB_DIR / "pybgworker.db"))
bg_utils.DB_PATH = os.environ["PYBGWORKER_DB"]


@task(name=TASK_LOG_TODO_CREATED)
def log_todo_created(title: str) -> None:
    time.sleep(10)
    print(f"[pybgworker] Todo created: {title}")
