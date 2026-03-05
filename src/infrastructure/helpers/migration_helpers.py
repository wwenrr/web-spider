from pathlib import Path
from typing import Final

from peewee_migrate import Router

from infrastructure.constants.db import DB_FILE_PATH
from infrastructure.database import database

MIGRATIONS_DIR_NAME: Final[str] = "migrations"
SCHEMA_FILE_NAME: Final[str] = "schema.yml"
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
MIGRATIONS_DIR_PATH: Final[Path] = PROJECT_ROOT / "db" / MIGRATIONS_DIR_NAME
SCHEMA_FILE_PATH: Final[Path] = PROJECT_ROOT / "db" / SCHEMA_FILE_NAME


def run_migrations() -> None:
    router = Router(database, migrate_dir=str(MIGRATIONS_DIR_PATH))
    router.run()
    _dump_schema()


def _dump_schema() -> None:
    try:
        from sqliteschema import SQLiteSchemaExtractor
    except ImportError:
        print("[migration] sqliteschema not found; skipping schema dump to db/schema.yml")
        return

    SCHEMA_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    extractor = SQLiteSchemaExtractor(str(DB_FILE_PATH))
    SCHEMA_FILE_PATH.write_text(extractor.dumps(output_format="yaml", verbosity_level=0))
