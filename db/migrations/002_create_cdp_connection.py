from typing import Any

from peewee_migrate import Migrator

from models.cdp_connection import CdpConnection


def migrate(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.create_tables([CdpConnection], safe=True)


def rollback(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.drop_tables([CdpConnection], safe=True)
