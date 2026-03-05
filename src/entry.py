import os
import signal
import sys
import time
from subprocess import CalledProcessError, run as subprocess_run
from typing import Final


WEB_APP_MODULE: Final[str] = "web_app"
APP_PORT: Final[int] = 3000


def run() -> None:
    _free_port(APP_PORT)
    completed = subprocess_run(
        [
            sys.executable,
            "-B",
            "-m",
            WEB_APP_MODULE,
        ],
        check=False,
        env=os.environ.copy(),
    )

    if completed.returncode != 0:
        raise CalledProcessError(
            completed.returncode,
            completed.args,
        )


def _free_port(port: int) -> None:
    for pid in _list_listening_pids(port):
        if pid == os.getpid():
            continue
        _terminate_pid(pid)


def _list_listening_pids(port: int) -> list[int]:
    completed = subprocess_run(
        ["lsof", "-ti", f"tcp:{port}", "-sTCP:LISTEN"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode not in {0, 1}:
        return []

    pids: list[int] = []
    for line in completed.stdout.splitlines():
        raw = line.strip()
        if raw.isdigit():
            pids.append(int(raw))
    return pids


def _terminate_pid(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except PermissionError:
        return

    if _wait_pid_exit(pid):
        return

    try:
        os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    except PermissionError:
        return

    _wait_pid_exit(pid)


def _wait_pid_exit(pid: int, timeout_seconds: float = 2.0) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        except PermissionError:
            return False
        time.sleep(0.05)
    return False
