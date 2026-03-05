from peewee import Model

from infrastructure.database import database


class BaseModel(Model):  # type: ignore[misc]
    class Meta:
        database = database
