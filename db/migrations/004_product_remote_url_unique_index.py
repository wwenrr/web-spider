from typing import Any

from peewee_migrate import Migrator

INDEX_NAME = "uq_product_remote_url"


def migrate(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.execute_sql(f"CREATE UNIQUE INDEX IF NOT EXISTS {INDEX_NAME} ON product (remote_url)")


def rollback(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.execute_sql(f"DROP INDEX IF EXISTS {INDEX_NAME}")
