from typing import Any, Final

from peewee_migrate import Migrator

from app.db.models import Todo


TODO_TABLE_NAME: Final[str] = "todo"


def migrate(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.create_tables([Todo], safe=True)


def rollback(migrator: Migrator, database: Any, fake: bool = False, **kwargs: Any) -> None:
    if fake:
        return

    database.drop_tables([Todo], safe=True)

