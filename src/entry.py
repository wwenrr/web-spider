import os
import sys
from subprocess import CalledProcessError, run as subprocess_run
from typing import Final


NICEGUI_MODULE: Final[str] = "nicegui_main"


def run() -> None:
    completed = subprocess_run(
        [
            sys.executable,
            "-B",
            "-m",
            NICEGUI_MODULE,
        ],
        check=False,
        env=os.environ.copy(),
    )

    if completed.returncode != 0:
        raise CalledProcessError(
            completed.returncode,
            completed.args,
        )
