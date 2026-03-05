from pathlib import Path
from typing import Final
import os
import sys
import time
from subprocess import CalledProcessError, run as subprocess_run

from infrastructure.constants.db import DB_DIR_PATH
from infrastructure.constants.queue import DEFAULT_WORKER_APP_NAME, TASK_LOG_TODO_CREATED

# Ensure pybgworker uses db/data/pybgworker.db in this process
DB_DIR: Final[Path] = DB_DIR_PATH
DB_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("PYBGWORKER_DB", str(DB_DIR / "pybgworker.db"))

from pybgworker import utils as bg_utils
bg_utils.DB_PATH = os.environ["PYBGWORKER_DB"]

from pybgworker.task import task

@task(name=TASK_LOG_TODO_CREATED)  # type: ignore[untyped-decorator]
def log_todo_created(title: str) -> None:
    time.sleep(10)
    print(f"[pybgworker] Todo created: {title}")


def run_worker() -> None:
    """
    Convenience entry point so `poetry run bgworker`
    will start a worker bound to `tasks`, storing its DB under db/data/.
    """
    db_dir = Path("db") / "data"
    db_dir.mkdir(parents=True, exist_ok=True)

    env = {
        **os.environ,
        # Configure pybgworker DB location via environment variable
        "PYBGWORKER_DB": str(db_dir / "pybgworker.db"),
    }

    completed = subprocess_run(
        [
            sys.executable,
            "-m",
            "pybgworker.cli",
            "run",
            "--app",
            DEFAULT_WORKER_APP_NAME,
        ],
        check=False,
        env=env,
    )

    if completed.returncode != 0:
        raise CalledProcessError(completed.returncode, completed.args)
