from pathlib import Path
import os
import sys
from subprocess import CalledProcessError, run as subprocess_run

from infrastructure.constants.queue import DEFAULT_WORKER_APP_NAME
from infrastructure.helpers.settings import get_bgworker_concurrency


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
    if "PYBGWORKER_CONCURRENCY" not in env:
        env["PYBGWORKER_CONCURRENCY"] = str(get_bgworker_concurrency())

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
