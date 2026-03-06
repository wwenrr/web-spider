from typing import Any

from peewee_migrate import Migrator

from infrastructure.models.category_crawl_job import CategoryCrawlJob


def migrate(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.create_tables([CategoryCrawlJob], safe=True)


def rollback(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.drop_tables([CategoryCrawlJob], safe=True)
