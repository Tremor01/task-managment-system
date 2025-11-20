from .postgres import PostgresRepository
from db.models import Task


class TaskRepository(PostgresRepository[Task]):
    MODEL = Task

