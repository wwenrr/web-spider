from typing import Any

from peewee_migrate import Migrator

from infrastructure.models.product import Product


def migrate(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.create_tables([Product], safe=True)


def rollback(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.drop_tables([Product], safe=True)
