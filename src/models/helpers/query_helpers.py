from models.todo import Todo


def todo_order_by_latest():
    return Todo.created_at.desc()
