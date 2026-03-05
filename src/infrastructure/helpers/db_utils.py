from infrastructure.database import database


def ping_database() -> bool:
    try:
        database.connect(reuse_if_open=True)
        return True
    finally:
        if not database.is_closed():
            database.close()
