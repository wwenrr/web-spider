from pathlib import Path
from typing import Final

DEFAULT_DB_FILE_NAME: Final[str] = "database.db"
DB_DIR_PATH: Final[Path] = Path("db") / "data"
DB_FILE_PATH: Final[Path] = DB_DIR_PATH / DEFAULT_DB_FILE_NAME
