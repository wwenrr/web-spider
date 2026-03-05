import subprocess
import sys


def run() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "importlinter.cli", "--config", ".importlinter"],
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
