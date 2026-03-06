from typing import Any

from peewee_migrate import Migrator

INDEX_NAME = "uq_category_crawl_job_active_normalized_url"


def migrate(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.execute_sql(
        "CREATE UNIQUE INDEX IF NOT EXISTS "
        f"{INDEX_NAME} ON category_crawl_job (normalized_category_url) "
        "WHERE crawl_status IN ('pending', 'processing')"
    )


def rollback(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.execute_sql(f"DROP INDEX IF EXISTS {INDEX_NAME}")
